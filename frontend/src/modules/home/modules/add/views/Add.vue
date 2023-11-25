<template>
    <v-row>
        <v-col cols="12">
            <v-card>
                <v-card-title class="ma-4">
                    <h3>Adicionar Dispositivo</h3>
                </v-card-title>
                <v-card-text>
                    <!--Formulário para adicionar dados de conexão-->
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-container>
                            <v-row>
                                <v-col cols="12" md="6">
                                    <v-text-field v-model="hostname" label="Endereço IP" type="text" :rules="hostnameRules"
                                        required></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <!--Travar o valor de entrada para ficar entre 1 e 65535-->
                                    <v-text-field v-model.number="port" label="Porta" type="number" :rules="portRules"
                                        min="1" max="65535" required></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-text-field v-model="username" label="Usuário" :rules="usernameRules"
                                        required></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-text-field v-model="password" label="Senha" outlined
                                        :rules="passwordRules"
                                        :append-inner-icon="state.showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                            :type="state.showPassword ? 'text' : 'password'"
                                            @click:append-inner="state.showPassword = !state.showPassword"
                                        ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="4">
                                    <v-select v-model="deviceDriver" :items="drivers" label="Driver"
                                        :rules="deviceDriverRules" required></v-select>
                                </v-col>
                                <v-col cols="12" md="4">
                                    <v-text-field v-model="deviceName" label="Nome do Dispositivo"
                                        :rules="deviceNameRules" required></v-text-field>
                                </v-col>
                                <v-col cols="12" md="4">
                                    <v-select v-model="deviceType" :items="types" label="Tipo de Dispositivo"
                                        :rules="deviceTypeRules" required></v-select>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-form>
                </v-card-text>


                <v-snackbar v-model="state.showSnackbar" multi-line location="bottom">
                    {{ state.detail }}

                    <template v-slot:actions>
                        <v-btn color="red" variant="text" @click="state.showSnackbar = false">
                            Fechar
                        </v-btn>
                    </template>
                </v-snackbar>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn variant="flat" prepend-icon="mdi-content-save" color="primary" :loading="state.isLoading" @click="save">Salvar</v-btn>
                </v-card-actions>
            </v-card>

        </v-col>
    </v-row>
</template>

<script setup>

import { ref } from 'vue';
import { useDeviceStore } from '@/store/device';

const deviceStore = useDeviceStore();

const form = ref(null); //variável para armazenar o formulário
const valid = ref(false); //variável para armazenar se o formulário é válido

const hostname = ref(''); //variável para armazenar o endereço IP
const port = ref(22); //variável para armazenar a porta
const username = ref(''); //variável para armazenar o usuário
const password = ref(''); //variável para armazenar a senha
const deviceDriver = ref(''); //variável para armazenar o driver
const deviceType = ref(''); //variável para armazenar o tipo de dispositivo
const deviceName = ref(''); //variável para armazenar o nome do dispositivo

const state = ref({
    showSnackbar: false,
    showPassword: false,
    isLoading: false,
    detail: '',
});


// Lista de Drivers
const drivers = [
    'ios',
    'iosxr',
    'nxos',
    'junos'
];

// Lista de Tipos de Dispositivos
const types = [
    'switch',
    'router',
];

// Rules
const hostnameRules = [
    v => !!v || 'Endereço IP é obrigatório',
    // Validar se o hostname é um endereço IP
    v => {
        const regex = new RegExp('\\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\\.|$)){4}\\b');
        return regex.test(v) || 'Informe um endereço IP válido';
    }
];

const portRules = [
    v => !!v || 'A porta é obrigatória',
    v => {
        const validPortRegex = /^(?:[1-9]\d{0,3}|[1-5]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$/;
        return validPortRegex.test(v) || 'Informe uma porta válida (entre 1 e 65535)';
    }
];

const usernameRules = [
    v => !!v || 'O usuário é obrigatório',
    // Permitir apenas letras, números, underline e hífen
    v => /^[a-zA-Z0-9_-]*$/.test(v) || 'O usuário não pode conter caracteres especiais'
];

const passwordRules = [
    v => !!v || 'A senha é obrigatória',
];

const deviceDriverRules = [
    v => !!v || 'O driver é obrigatório',
];

const deviceTypeRules = [
    v => !!v || 'O tipo de dispositivo é obrigatório',
];

const deviceNameRules = [
    v => !!v || 'O nome do dispositivo é obrigatório',
];


const save = async () => {
    try {
        state.value.isLoading = true;
        const data = {
            hostname: hostname.value,
            port: Number(port.value),
            username: username.value,
            password: password.value,
            driver_name: deviceDriver.value,
            device_type: deviceType.value,
            device_name: deviceName.value,
        };

        await deviceStore.createDevice(data);

        state.value.showSnackbar = true;
        state.value.detail = 'Dispositivo adicionado com sucesso';

        // Limpar os campos do formulário
        [hostname, username, password, deviceDriver, deviceType].forEach(field => field.value = '');

        // Resetar o formulário
        form.value.reset();

    } catch (error) {
        state.value.showSnackbar = true;
        state.value.detail = error.response.data.detail;
        console.log(error.response.data.detail);
        state.value.isLoading = false;
    }finally{
        state.value.isLoading = false;
    }
}

</script>

<script>
export default {
    name: "AddPage",
}
</script>