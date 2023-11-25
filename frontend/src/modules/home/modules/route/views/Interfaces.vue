<template>
    <v-container>
        <v-card variant="flat">
            <v-card-title>
                <h3>Configuração de interface de rede</h3>
            </v-card-title>

            <v-card-text>
                <v-form>
                    <v-row>
                        <!--Device-->
                        <v-col cols="12" md="6">
                            <v-select v-model="selectedDevice" :items="devicesNames" label="Dispositivo" item-text="name"
                                item-value="id" @update:model-value="getInterfaces"></v-select>
                        </v-col>
                        <!--Switch para alternar entre criar loopback ou listar as interfaces do dispositivos-->
                        <v-col cols="12" md="6">
                            <v-switch v-model="state.isLoopback" label="Loopback" color="primary"></v-switch>
                        </v-col>

                        <!--Se Loopback-->
                        <template v-if="state.isLoopback">
                            <!--Loopback value/name-->
                            <v-col cols="12" md="6">
                                <v-text-field v-model="selectedInterface" label="Loopback"></v-text-field>
                            </v-col>

                            <!--IP-->
                            <v-col cols="12" md="6">
                                <v-text-field v-model="ip" label="Endereço IP"></v-text-field>
                            </v-col>
                            <!--NetMask-->
                            <v-col cols="12" md="6">
                                <v-text-field v-model="mask" label="Máscara"></v-text-field>
                            </v-col>
                            <!--Description-->
                            <v-col cols="12" md="6">
                                <v-text-field v-model="description" label="Descrição"></v-text-field>
                            </v-col>
                        </template>

                        <!--Se Interface-->
                        <template v-else>
                            <!--Interface-->
                            <!--Interface-->
                            <v-col cols="12" md="6">
                                <v-select v-model="selectedInterface" :items="interfacesNames" label="Interface"
                                    item-text="name" item-value="name" @update:model-value=""
                                ></v-select>
                            </v-col>
                            <!--IP-->
                            <v-col cols="12" md="6">
                                <v-text-field v-model="ip" label="Endereço IP"></v-text-field>
                            </v-col>
                            <!--NetMask-->
                            <v-col cols="12" md="6">
                                <v-text-field v-model="mask" label="Máscara"></v-text-field>
                            </v-col>
                            <!--Description-->
                            <v-col cols="12" md="6">
                                <v-text-field v-model="description" label="Descrição"></v-text-field>
                            </v-col>
                        </template>

                        <!--Select Partition of the destination file system ['unix:', ...]-->
                        <v-col cols="12" md="6">
                            <v-select v-model="selectedPartition" :items="partitions"
                                label="Partição de destino da configuração" item-text="name" item-value="name"></v-select>
                        </v-col>
                        <!--Add button-->
                        <v-col cols="12" md="6">
                            <v-btn color="primary" :disabled="state.isLoading" @click="addInterface">
                                Adicionar
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>

        <!-- Tela de carregamento -->
        <v-overlay :model-value="state.isLoading" class="align-center justify-center">
            <v-progress-circular color="primary" indeterminate size="64">
            </v-progress-circular>
        </v-overlay>

        <v-alert v-if="state.message" :value="state.status" :type="state.status ? 'success' : 'error'" closable>
            {{ state.message }}
        </v-alert>
    </v-container>
</template>

<script setup>

import { ref, onBeforeMount } from 'vue'

import { useDeviceStore } from '@/store/device';
import { useNapalmStore } from '@/store/napalm';

const deviceStore = useDeviceStore()
const napalmStore = useNapalmStore()

const state = ref({
    isLoading: false,
    status: false,
    message: null,
    isLoopback: false,
})

const devices = ref([])
const devicesNames = ref([])
const interfacesNames = ref([])
const interfaces = ref([])
const partitions = ref(['unix:', 'system:'])

const selectedDevice = ref(null)
const selectedInterface = ref(null)
const selectedDeviceData = ref(null)
const selectedPartition = ref('unix:')

const responseData = ref(null)

const ip = ref(null)
const mask = ref(null)
const description = ref(null)


const getDevices = async () => {
    //Clear devices names
    devicesNames.value = []

    await deviceStore.getDevices()
    devices.value = deviceStore.devices

    //Get devices names
    for (const [key, value] of Object.entries(devices.value)) {

        if (value.device_type === 'router') {
            devicesNames.value.push(value.device_name)
        }
    }
}

const getInterfaces = async () => {
    //Clear interfaces names
    interfacesNames.value = []
    //Get device data
    for (const [key, value] of Object.entries(devices.value)) {
        if (value.device_name === selectedDevice.value) {
            selectedDeviceData.value = value
        }
    }

    //Mount request data
    const device = {
        hostname: selectedDeviceData.value.hostname,
        username: selectedDeviceData.value.username,
        password: selectedDeviceData.value.password,
        driver: selectedDeviceData.value.driver_name,
        optional_args: {
            port: Number(selectedDeviceData.value.port),
        },
    }


    //Get interfaces
    state.value.isLoading = true
    await napalmStore.getFacts(device)
    state.value.isLoading = false

    // Filter interfaces in data
    interfaces.value = napalmStore.data.interfaces

    //Get interfaces names
    for (const [key, value] of Object.entries(interfaces.value)) {
        interfacesNames.value.push(value.name)
    }
}


const addInterface = async () => {
    //Clear message
    state.value.message = ''
    state.value.status = false
    responseData.value = {}

    try {
        //Mount request data
        const device = {
            hostname: selectedDeviceData.value.hostname,
            username: selectedDeviceData.value.username,
            password: selectedDeviceData.value.password,
            driver: selectedDeviceData.value.driver_name,
            optional_args: {
                port: Number(selectedDeviceData.value.port),
                dest_file_system: selectedPartition.value,
            },
        }

        const data = {
            interface_name: selectedInterface.value,
            description: description.value,
            ip_address: ip.value,
            netmask: mask.value,
        }

        const request = {
            credentials: device,
            configurations: data,
        }

        //Send request
        state.value.isLoading = true
        await napalmStore.Interfaces(request)

        //Get response data
        responseData.value = napalmStore.data

        //Set message
        state.value.message = responseData.value.message
        state.value.status = responseData.value.status
        state.value.isLoading = false
    } catch (error) {
        state.value.message = error.message
        state.value.status = false
        state.value.isLoading = false
    }
}


onBeforeMount(async () => {
    await getDevices()
})



</script>

<script>
export default {
    name: 'Interfaces',
}
</script>