<template>
    <v-app :theme="themeStore.theme">
        <v-container fluid class="fill-height">
            <v-row>
                <v-col cols="12" md="4" class="mx-auto">
                    <v-card class="elevation-12" :loading="isLoading">
                        <v-toolbar color="primary">
                            <v-toolbar-title class="text-uppercase">
                                <span class="font-weight-bold">{{ isRegister ? 'Registro' : 'Login' }}</span>
                            </v-toolbar-title>
                            <v-spacer></v-spacer>
                            <!--Botão para Trocar Tema-->
                            <v-btn icon @click="themeStore.toggleTheme">
                                <v-icon>mdi-lightbulb</v-icon>
                            </v-btn>
                        </v-toolbar>
    
                        <v-card-text class="px-12 py-8">
                            <v-form ref="form" v-model="valid" lazy-validation>
                                <v-text-field
                                    v-if="isRegister"
                                    label="Nome de usuário"
                                    prepend-icon="mdi-account"
                                    v-model="username"
                                    variant="outlined"
                                    :rules="nameRules"
                                    required
                                    ></v-text-field>
                                <v-text-field
                                    class="mt-4"
                                    label="E-mail"
                                    prepend-icon="mdi-email"
                                    v-model="email"
                                    variant="outlined"
                                    :rules="emailRules"
                                    type="email"
                                    required
                                ></v-text-field>
                                <v-text-field
                                    class="mt-4"
                                    label="Senha"
                                    prepend-icon="mdi-lock"
                                    v-model="password"
                                    variant="outlined"
                                    :rules="passwordRules"
                                    :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                    :type="showPassword ? 'text' : 'password'"
                                    @click:append-inner="showPassword = !showPassword"
                                ></v-text-field>
                            </v-form>
                        </v-card-text>
    
                        <v-snackbar v-model="state.showSnackbar" multi-line location="top">
                                {{ state.detail }}
    
                                <template v-slot:actions>
                                    <v-btn color="red" variant="text" @click="state.showSnackbar = false">
                                        Fechar
                                    </v-btn>
                                </template>
                        </v-snackbar>
    
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                color="primary"
                                text
                                @click="isRegister = !isRegister"
                            >
                                {{ isRegister ? 'Já tenho uma conta' : 'Criar uma conta' }}
                            </v-btn>
                            <v-btn
                                color="primary"
                                text
                                @click="isRegister ? register() : login()"
                                :disabled="!valid"
                            >
                                {{ isRegister ? 'Registrar' : 'Entrar' }}
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-app>
    </template>
    
    <script setup>
    import { ref } from "vue";
    import {useThemeStore} from '@/store/theme';
    import {useAuthStore} from '@/store/auth';
    import {useUserStore} from '@/store/user';
    import http from '@/services/http';
    import router from "@/router";
    
    const themeStore = useThemeStore();
    const authStore = useAuthStore();
    const userStore = useUserStore();
    
    
    const isRegister = ref(false); // Variável para controlar se o usuário está na tela de login ou registro
    const username = ref(''); // Variável para armazenar o nome de usuário
    const email = ref(''); // Variável para armazenar o e-mail
    const password = ref(''); // Variável para armazenar a senha
    const showPassword = ref(false); // Variável para controlar se a senha está visível ou não
    const isLoading = ref(false); // Variável para controlar o loading
    const state = ref({
        showSnackbar: false,
        detail: '',
    }); // Variável para controlar o snackbar
    
    // Variável para controlar se o formulário é válido ou não
    const valid = ref(false);
    
    
    // Rules para validação do formulário
    const nameRules = [
        (v) => !!v || 'Nome é obrigatório', // Verifica se o campo está vazio
        // Nome não pode ter caracteres especiais ou números
        (v) => /^[a-zA-ZÀ-ú\s]+$/.test(v) || 'Nome não pode conter números ou caracteres especiais',
    ];
    
    const emailRules = [
        (v) => !!v || 'E-mail é obrigatório', // Verifica se o campo está vazio
        (v) => /.+@.+\..+/.test(v) || 'E-mail deve ser válido', // Verifica se o e-mail é válido
    ];
    
    const passwordRules = [
        (v) => !!v || 'Senha é obrigatória', // Verifica se o campo está vazio
        (v) => v.length >= 8 || 'Senha deve ter no mínimo 8 caracteres', // Verifica se a senha tem no mínimo 8 caracteres
    ];
    
    
    // Função para fazer login
    
    
    
    const login = async () => {
        try {
            // Verifica se o formulário é válido
            if (valid.value) {
                isLoading.value = true;
    
                const form = new FormData();
    
                form.append('username', email.value);
                form.append('password', password.value);
    
                const { data } = await http.post('users/login', form, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
    
                authStore.setToken(data.access_token, data.token_type);
    
                state.value.showSnackbar = true;
                state.value.detail = 'Login realizado com sucesso';
    
                setTimeout(() => {
                    router.push(router.currentRoute.value.query.redirect || '/home');
                }, 1000);
            }
    
        } catch (error) {
            state.value.showSnackbar = true;
            console.log(error);
            state.value.detail = error.response.data.detail;
        } finally {
            isLoading.value = false;
        }
    };
    
    const register = () => {
        try {
            isLoading.value = true;
    
            userStore.createUser({
                username: username.value,
                email: email.value,
                password: password.value,
            });
    
            state.value.showSnackbar = true;
            state.value.detail = 'Registro realizado com sucesso';
    
        } catch (error) {
            state.value.showSnackbar = true;
            state.value.detail =  error.response.data.detail;
        } finally {
            isLoading.value = false;
        }
    };
    
    </script>
    
    <script>
    export default {
        name: "LoginPage",
    };
    </script>
    