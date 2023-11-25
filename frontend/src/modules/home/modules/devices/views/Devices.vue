<template>
    <v-row>
        <v-col cols=12>
            <v-card class="elevation-0">
                <v-card-title>
                    <v-row>
                        <v-col>
                            <h3>Últimos dispositivos cadastrados.</h3>
                        </v-col>

                        <v-col cols="12" sm="6" md="4">
                            <v-text-field
                                v-model="search"
                                append-inner-icon="mdi-magnify"
                                label="Pesquisar"
                                variant="outlined"
                            ></v-text-field>
                        </v-col>

                    </v-row>
                </v-card-title>

                <v-card-text>
                    <v-data-table
                        :headers="headers"
                        :items="devices"
                        :search="search"
                        :no-data-text="state.isLoading ? '' : 'Nenhum dispositivo cadastrado.'"
                        :loading-text="state.isLoading ? 'Carregando...' : ''"
                        :footer-props="{
                            itemsPerPageOptions: [5, 10, 25, 50, 100],
                            showCurrentPage: true,
                            showFirstLastPage: true
                        }"
                        :items-per-page="10"
                        :server-items-length="totalDevices"
                        :options.sync="options"
                        >

                        <!--Slot para exibir ou ocultar a senha-->
                        <template v-slot:item.password="{ item }">
                            <v-chip
                                color="primary"
                                @click="state.showPassword = !state.showPassword"
                            >
                                <template v-if="state.showPassword">
                                    {{ item.password }}
                                </template>
                                <template v-else>
                                    ***********
                                </template>
                            </v-chip>
                        </template>

                        
                        <!--Slot para personalizar o texto do driver-->
                        <template v-slot:item.driver_name="{ item }">
                            <span v-if="item.driver_name === 'ios'" class="font-weight-bold">Cisco IOS</span>
                            <span v-else-if="item.driver_name === 'iosxr'" class="font-weight-bold">Cisco IOS XR</span>
                            <span v-else-if="item.driver_name === 'nxos'" class="font-weight-bold">Cisco NX-OS</span>
                            <span v-else-if="item.driver_name === 'junos'" class="font-weight-bold">Juniper JunOS</span>
                            <span v-else-if="item.driver_name === 'eos'" class="font-weight-bold">Arista EOS</span>
                        </template>

                        <!--Slot para exibir o icone router ou switch no tipo-->
                        <template v-slot:item.device_type="{ item }">
                            <v-icon size="x-large" color="grey-darken-1" v-if="item.device_type === 'router'">mdi-router</v-icon>
                            <v-icon size="x-large" color="blue-grey-darken-1" v-else>mdi-switch</v-icon>
                        </template>

                        <!--Slot para personalizar font e cor do nome do dispositivo-->
                        <template v-slot:item.device_name="{ item }">
                            <span v-if="item.device_type === 'router'" class="font-weight-bold text-primary">{{ item.device_name }}</span>
                            <span v-else class="font-weight-bold text-secondary">{{ item.device_name }}</span>
                        </template>

                        <!--Slot para personalizar font e cor do endereço IP-->
                        <template v-slot:item.hostname="{ item }">
                            <span v-if="item.device_type === 'router'" class="font-weight-bold text-primary">{{ item.hostname }}</span>
                            <span v-else class="font-weight-bold text-secondary">{{ item.hostname }}</span>
                        </template>

                        <!--Slot para personalizar cor vermelha para porta-->
                        <template v-slot:item.port="{ item }">
                            <span class="text-red font-weight-bold">{{ item.port }}</span>
                        </template>

                        <!--Slot para personalizar icone e cor para usuário-->
                        <template v-slot:item.username="{ item }">
                            <v-icon size="x-small" color="grey-darken-1" >mdi-penguin</v-icon>
                            <span class="font-weight-bold">{{ item.username }}</span>
                        </template>

                        <!-- Ações -->
                        <template v-slot:item.actions="{ item }">
                            <v-icon
                                small
                                class="mr-2"
                                @click=" state.selectedDevice=item; getConfig();"
                            >
                                mdi-eye
                            </v-icon>
                            <v-icon
                                small
                                class="mr-2"
                                @click="editDevice(item)"
                            >
                                mdi-pencil
                            </v-icon>
                            <v-icon
                                small
                                @click="state.selectedDevice = item; state.showDeleteDialog = true;"
                            >
                                mdi-delete
                            </v-icon>
                        </template>
                    </v-data-table>
                </v-card-text>
                
                <!--Dialog para deletar-->
                <v-dialog v-model="state.showDeleteDialog" max-width="500px">
                    <v-card>
                        <v-card-title class="headline">Deletar Dispositivo</v-card-title>
                        <v-card-text>
                            <span>Tem certeza que deseja deletar o <strong>{{ state.selectedDevice?.device_type }}</strong> <strong>{{ state.selectedDevice?.device_name }}</strong>?</span>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="state.showDeleteDialog = false">Cancelar</v-btn>
                            <v-btn color="blue darken-1" text @click="deleteDevice">Deletar</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <!--Dialog para Informações do dispositivo-->
                <v-dialog
                    v-model="state.showInfoDialog"
                    fullscreen
                    persistent
                    :scrim="false"
                    hide-overlay
                    transition="dialiog-bottom-transition"
                >
                <v-card>
                    <v-card-title class="headline">Informações do dispositivo</v-card-title>
                    <v-card-text>
                        <v-container class="mb-4">
                            <v-row>
                                <v-col>
                                    <h2>Informações básicas</h2>
                                </v-col>
                            </v-row>

                            <v-table>
                                <thead>
                                    <tr>
                                        <th v-for="header in headerVendor" :key="header.value">
                                            {{ header.title }}
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td class="font-weight-bold">{{ config.vendor }}</td>
                                        <td class="text-red-darken-3">{{ config.model }}</td>
                                        <td class="font-weight-light">{{ config.os_version }}</td>
                                        <td class="text-cyan-darken-3">{{ config.serial_number }}</td>
                                        <td class="text-green-darken-3">{{ config.uptime }}</td>
                                        <td>{{ config.hostname }}</td>
                                        <td>{{ config.fqdn }}</td>
                                    </tr>
                                </tbody>
                            </v-table>
                        </v-container>

                        <!--INTERFACES-->
                        <v-container class="mb-4">

                            <v-row>
                                <v-col>
                                    <h2>Interfaces de Rede</h2>
                                </v-col>
                            </v-row>

                            <v-table>
                                <thead>
                                    <tr>
                                        <th class="text-center" v-for="header in headerInterfaces" :key="header.value">{{ header.title }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!--Percorre interfaces-->
                                    <tr v-for="iface in interfaces" :key="iface.name">
                                        <td class="text-center">{{ iface.name }}</td>
                                        <td class="text-center">{{ iface.mac_address }}</td>
                                        <td class="text-center">{{ Object.keys(iface.ipv4)[0] }}</td>
                                        <td class="text-center">{{ Object.keys(iface.ipv6)[0] }}</td>
                                        <td class="text-center">{{ iface.description }}</td>

                                        <!--Verifica se a interface está habilitada e adicionar icone-->
                                        <td class="text-center">
                                            <v-icon size="x-large" color="green-darken-1" v-if="iface.is_enabled">mdi-check</v-icon>
                                            <v-icon size="x-large" color="red-darken-1" v-else>mdi-close</v-icon>
                                        </td>

                                        <!--Verifica se a interface está up e adicionar icone-->
                                        <td class="text-center">
                                            <v-icon size="x-large" color="green-darken-1" v-if="iface.is_up">mdi-arrow-up-bold</v-icon>
                                            <v-icon size="x-large" color="red-darken-1" v-else>mdi-arrow-down-bold</v-icon>
                                        </td>
                                        <td class="text-center">{{ iface.speed }}</td>
                                    </tr>
                                </tbody>
                            </v-table>

                        </v-container>

                        <!--ARP TABLE-->
                        <v-container class="mb-4">
                            <v-row>
                                <v-col>
                                    <h2>Tabela ARP</h2>

                                    <v-data-table
                                        items-per-page="10"
                                        :headers="headerArp"
                                        :items="config.arp_table"
                                        :loading="state.isLoading"
                                        :sort-by="[{key: 'ip', order: 'asc'}]"
                                        >
                                    </v-data-table>
                                </v-col>
                            </v-row>
                        </v-container>

                        <!--CONFIGURAÇÃO-->
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <h2>Configuração</h2>
                                </v-col>
                                <v-col cols="12">
                                    <v-textarea
                                        v-model="config.running_config.running"
                                        label="Running-config"
                                        readonly
                                        rows="20"
                                        class="font-weight-light"
                                    ></v-textarea>
                                </v-col>
                            </v-row>
                        </v-container>

                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" variant="flat" @click="state.showInfoDialog = false;">Fechar</v-btn>
                    </v-card-actions>
                </v-card>
                </v-dialog>

                <!-- Tela de carregamento -->
                <v-overlay :model-value="state.isLoading" class="align-center justify-center">
                    <v-progress-circular color="primary" indeterminate size="64">
                    </v-progress-circular>
                </v-overlay>


                <!-- SnackBar para exibir mensagens -->
                <v-snackbar v-model="state.showSnackbar" multi-line location="bottom">
                    {{ state.detail }}

                    <template v-slot:actions>
                        <v-btn color="red" variant="text" @click="state.showSnackbar = false">
                            Fechar
                        </v-btn>
                    </template>
                </v-snackbar>
                
            </v-card>

        </v-col>
    </v-row>

</template>

<script setup>
import {ref, onBeforeMount} from 'vue';

import { VDataTable } from 'vuetify/lib/components/VDataTable/VDataTable.mjs';
import { useDeviceStore } from '@/store/device';
import { useNapalmStore } from '@/store/napalm';

const deviceStore = useDeviceStore();
const napalmStore = useNapalmStore();


const devices = ref([]);
const interfaces = ref({});
const search = ref('');
const config = ref({});
const totalDevices = ref(0);


const options = ref({
    page: 1,
    itemsPerPage: 10,
    sortBy: ['hostname'],
    sortDesc: [false]
});


const state = ref({
    isLoading: false,
    showPassword: false,
    showSnackbar: false,
    selectedDevice: null,
    showInfoDialog: false,
    showDeleteDialog: false,
    detail: ''
});

// Cabeçalhos da tabela
const headers = [
    { title: 'Endereço IP', align: 'start', key: 'hostname'},
    { title: 'Porta', align: 'start', key: 'port'},
    { title: 'Nome', align: 'start', key: 'device_name'},
    { title: 'Tipo', align: 'start', key: 'device_type'},
    { title: 'Driver', align: 'start', key: 'driver_name'},
    { title: 'Usuário', align: 'start', key: 'username'},
    { title: 'Senha', align: 'start', key: 'password'},
    { title: 'Ações', align: 'start', key: 'actions', sortable: false}
]

const headerArp = [
    { title: 'Interface', align:'start', key: 'interface' },
    { title: 'MAC', align:'start', key: 'mac' },
    { title: 'IP', align:'start', key: 'ip' },
    { title: 'Age', align:'start', key: 'age' },
];

const headerVendor = [
    { title: 'Fabricante', value: 'vendor' },
    { title: 'Modelo', value: 'model' },
    { title: 'Versão', value: 'os_version' },
    { title: 'Serial', value: 'serial_number' },
    { title: 'Uptime', value: 'uptime' },
    { title: 'Hostname', value: 'hostname' },
    { title: 'FQDN', value: 'fqdn' },
];

const headerInterfaces = [
    { title: 'Interface', value: 'name'},
    { title: 'MAC', value: 'mac_address' },
    { title: 'Ipv4', value: 'ipv4'},
    { title: 'Ipv6', value: 'ipv6'},
    { title: 'Descrição', value: 'description' },
    { title: 'Habilitada', value: 'is_enabled' },
    { title: 'Ativa', value: 'is_up' },
    { title: 'Speed', value: 'speed'}
];


// Carrega os dispositivos
const loadDevices = async() => {
    state.isLoading = true;
    await deviceStore.getDevices();
    devices.value = deviceStore.devices;
    state.isLoading = false;
}

const getConfig = async() => {

    const device = {
        hostname: state.value.selectedDevice.hostname,
        username: state.value.selectedDevice.username,
        password: state.value.selectedDevice.password,
        driver: state.value.selectedDevice.driver_name,
        optional_args: {
            port: Number(state.value.selectedDevice.port)
        }
    }

    state.value.isLoading = true;

    try{
        await napalmStore.getFacts(device);
        config.value = napalmStore.data;
        interfaces.value = napalmStore.data.interfaces;

        state.value.showInfoDialog = true;
        
    } catch (error) {
        state.value.detail = error;
        state.value.showSnackbar = true;
    }finally{
        state.value.isLoading = false;
    }

}

// Deleta o dispositivo
const deleteDevice = async() => {
    state.isLoading = true;

    try{
        state.value.isLoading = true;
        await deviceStore.deleteDevice(state.value.selectedDevice.uuid);
        state.value.showDeleteDialog = false;
        state.value.detail = 'Dispositivo deletado com sucesso!';
        state.value.showSnackbar = true;
        loadDevices();
    } catch (error) {
        state.value.detail = error;
        state.value.showSnackbar = true;
    }finally{
        state.value.isLoading = false;
    }
}

// Carrega os dispositivos antes de montar o componente
onBeforeMount(() => {
    loadDevices();
});

</script>


<script>

export default{
    name: 'DevicesPage'
}
</script>