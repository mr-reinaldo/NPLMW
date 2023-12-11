<template>
    <v-container>
        <v-card variant="flat">
            <v-card-title>
                <h3>Configuração de Rotas Estáticas</h3>
            </v-card-title>
            <v-card-text>
                <v-form>
                    <v-row>
                        <!--Device-->
                        <v-col cols="12" md="6">
                            <v-select v-model="selectedDevice" :items="devicesNames" label="Dispositivo" item-text="name"
                                item-value="id" @update:model-value="getInterfaces" :loading="state.isLoading"></v-select>
                        </v-col>
                        <!--Network-->
                        <v-col cols="12" md="6">
                            <v-text-field v-model="network" label="Rede" outlined dense></v-text-field>
                        </v-col>
                        <!--NetMask-->
                        <v-col cols="12" md="6">
                            <v-text-field v-model="mask" label="Máscara" outlined dense></v-text-field>
                        </v-col>
                        <!--Next Hop [Interface or IP] botton select option, and desblock input-->
                        <v-col cols="12" md="6">
                            <v-select v-model="selectedNextHop" :items="['Interface', 'IP']" label="Selecione o tipo de Next Hop"
                                item-text="name" item-value="name"></v-select>
                        </v-col>

                        <!--Next Hop [Interface or IP] conditional input if none disabled-->
                        <v-col cols="12" md="6">
                            <!--Se IP-->
                            <v-text-field v-model="nextHop" v-if="selectedNextHop === 'IP'"
                                label="Endereço IP"></v-text-field>
                            <!--Se Interface-->
                            <v-select v-model="nextHop" v-if="selectedNextHop === 'Interface'" :items="interfacesNames"
                                label="Interface" item-text="name"></v-select>
                            <!--Se Nenhum, Ocultar componente-->
                            <v-text-field v-if="selectedNextHop == null" disabled></v-text-field>

                        </v-col>

                        <!-- Select Partition of the destination file system ['unix:', ...]-->
                        <v-col cols="12" md="6">
                            <v-select v-model="selectedPartition" :items="partitions"
                                label="Partição de destino da configuração" item-text="name" item-value="name"></v-select>

                        </v-col>

                        <!--Add button-->
                        <v-col cols="12" md="6">
                            <v-btn color="primary" @click="addStaticRoute" :loading="state.isLoading"
                                :disabled="state.isLoading">
                                Adicionar
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>

            <v-alert v-if="state.message" :value="state.status" :type="state.status ? 'success' : 'error'" closable>
                {{ state.message }}
            </v-alert>

        </v-card>
    </v-container>
</template>

<script setup>

import { ref, onBeforeMount } from 'vue'
import { useDeviceStore } from '@/store/device';
import { useNapalmStore } from '@/store/napalm';

const deviceStore = useDeviceStore()
const napalmStore = useNapalmStore()

const devices = ref({})
const interfaces = ref({})
const responseData = ref({})


const selectedDevice = ref(null)
const selectedDeviceData = ref({
    hostname: '',
    username: '',
    password: '',
    optional_args: {
        port: Number(0),
    },

})
const selectedPartition = ref('unix:')
const selectedNextHop = ref(null)

const devicesNames = ref([])
const interfacesNames = ref([])
const network = ref('0.0.0.0')
const mask = ref('0.0.0.0')
const nextHop = ref('')


const state = ref({
    isLoading: false,
    isDisabled: false,
    message: '',
    status: false,
})

const partitions = [
    'unix:',
]



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
    interfaces.value = await napalmStore.data.data.interfaces

    //Get interfaces names
    for (const [key, value] of Object.entries(interfaces.value)) {
        interfacesNames.value.push(value.name)
    }
}


const addStaticRoute = async () => {
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
            route: network.value,
            mask: mask.value,
            next_hop: nextHop.value,
        }

        const request = {
            credentials: device,
            static_route: data,
        }

        //Send request
        state.value.isLoading = true
        await napalmStore.staticRoute(request)

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




onBeforeMount(() => {
    getDevices()
})


</script>

<script>
export default {
    name: 'StaticRoutes',
}
</script>