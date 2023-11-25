<template>
    <v-container fluid>
        <v-card>
            <v-card-title class="text-h6">
                <v-row>
                    <v-col cols="12" md="6">
                        <v-icon>mdi-home-analytics</v-icon>
                        Dashboard
                    </v-col>

                    <v-col cols="12" md="6" class="text-right">
                        <v-btn color="primary" text @click="refresh" :loading="isLoading">
                            <v-icon>mdi-refresh</v-icon>
                        </v-btn>
                    </v-col>
                </v-row>

            </v-card-title>
            <v-card-text class="mt-6">
                <!--Alert-->
                <v-alert class="mb-4" v-if="message" :value="status" :type="status ? 'success' : 'error'" variant="tonal" closable>
                    {{ message }}
                </v-alert>

                <!--Cards-->
                <v-row align="center" justify="center">
                    <v-col cols="12" md="4">
                        <CardInformation v-bind="CardTotal" />
                    </v-col>
                    <v-col cols="12" md="4">
                        <CardInformation v-bind="CardUp" />
                    </v-col>
                    <v-col cols="12" md="4">
                        <CardInformation v-bind="CardDown" />
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';

import CardInformation from '@/components/CardInformation.vue';
import { useDeviceStore } from '@/store/device';
import { useNapalmStore } from '@/store/napalm';

const deviceStore = useDeviceStore();
const napalmStore = useNapalmStore();

// Variáveis
const devices = ref({});
const ipAddressList = ref({});
const isLoading = ref(false);
const message = ref('');
const status = ref(false);



// Dados para os cards
const CardTotal = ref({
    title: 'Dispositivos registrados',
    total: 0,
    icon: 'router',
    color: 'primary',
})

const CardUp = ref({
    title: 'Dispositivos Ativos',
    total: 0,
    icon: 'arrow-up-bold',
    color: 'success',
})

const CardDown = ref({
    title: 'Dispositivos Inativos',
    total: 0,
    icon: 'arrow-down-bold',
    color: 'error',
})

// Função para pegar os hosts

const getDevices = async () => {
    await deviceStore.getDevices();

    devices.value = deviceStore.devices;

    // Percorre o array
    devices.value.forEach((device) => {
        ipAddressList.value[device.device_name] = device.hostname;
    });

    // Atualiza os cards
    CardTotal.value.total = devices.value.length;
}

// Função para realizar o teste de conexão
const testConnection = async () => {

    console.log(ipAddressList.value);
    await napalmStore.Ping(ipAddressList.value);

    const data = napalmStore.data;

    // Atualiza os cards
    CardUp.value.total = data.data.devices_up;
    CardDown.value.total = data.data.devices_down;
}



// Função para refresh
const refresh = async () => {
    isLoading.value = true;
    await getDevices();
    await testConnection();
    isLoading.value = false;
}


onBeforeMount(async () => {
    await getDevices();
    await testConnection();
});





</script>

<script>
export default {
    name: 'DashboardPage',
}
</script>