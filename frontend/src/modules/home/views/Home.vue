<template>
    <v-app :theme="themeStore.theme">
        <v-navigation-drawer v-model="drawer">

            <!-- Logo -->
            <template v-slot:prepend>
                <v-list class="mb-2">
                    <v-list-item prepend-icon="mdi-badge-account">
                        <v-list-item-title class="text-deep-orange-darken-3 font-weight-bold">Olá, {{ user.username }}</v-list-item-title>
                        <v-list-item-subtitle class="font-weight-medium">{{ user.email }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-divider class="mt-2"></v-divider>
                </v-list>
            </template>

            <!-- Menu -->
            <v-list densety="compact" nav v-for="item in menuItems" :key="item">
                <v-list-item ripple :to="item.url" :title="item.title" :value="item.value" :prepend-icon="item.icon"
                    :exact="item.exact" :active="item.value === $route.name" :disabled="item.disabled">
                </v-list-item>
            </v-list>
            <v-divider></v-divider>

            <!--Perfil-->
            <v-list dense nav>
                <v-list-item ripple prepend-icon="mdi-account" title="Meu Perfil" value="profile" to="/home/profile" exact :active="$route.name === 'profile'">
                </v-list-item>
            </v-list>


            <!-- Logout -->
            <template v-slot:append>
                <v-divider></v-divider>
                <div class="pa-2 ">
                    <v-btn prepend-icon="mdi-logout-variant" block text-center color="primary" @click="logout">
                        Sair
                    </v-btn>
                </div>

                <div class="text-center mt-2">
                    <small class="text-grey--text">
                        &copy; 2023 NPLMW
                    </small>
                </div>
            </template>
        </v-navigation-drawer>

        <v-app-bar elevation="0" class="border-b">
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

            <v-toolbar-title class="font-weight-bold text-amber-darken-4">NPLMW</v-toolbar-title>

            <v-spacer></v-spacer>
            <!--Alterar Tema-->
            <v-btn icon @click="themeStore.toggleTheme">
                <v-icon>mdi-lightbulb</v-icon>
            </v-btn>
        </v-app-bar>


        <!-- Conteúdo -->
        <v-main>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-main>
    </v-app>
</template>

<script setup>

import { ref, computed, onBeforeMount } from 'vue';
import { useThemeStore } from '@/store/theme';
import { useAuthStore } from '@/store/auth';
import router from '@/router';

const themeStore = useThemeStore(); // Tema do Vuetify
const authStore = useAuthStore(); // Autenticação do usuário

const drawer = ref(true); // true = open, false = close  (Navigation Drawer)

const user = ref({})



// Lista de items do menu
const menuItems = computed(() => [
    { title: 'Dashboard', icon: 'mdi-view-dashboard', url: '/home/dashboard', value: 'dashboard', exact: true, active: true, disabled:false },
    { title: 'Lista de Tarefas', icon: 'mdi-view-list', url: '/home/tasks', value: 'tasks', exact: true, disabled:true },
    { title: 'Roteadores', icon: 'mdi-router', url: '/home/route', value: 'route', exact: true, disabled:false },
    { title: 'Switches', icon: 'mdi-switch', url: '/home/switch', value: 'switch', exact: true, disabled:true},
    { title: 'Adicionar Dispositivo', icon: 'mdi-server-plus', url: '/home/devices/add', value: 'add', exact: true, disabled:false},
    { title: 'Dispositivos', icon: 'mdi-server', url: '/home/devices', value: 'devices', exact: true , disabled:false},
]);


// Função para fazer logout
const logout = () => {
    authStore.logout();

    // Redireciona para a página de login
    router.push({ name: 'login' });
};

// Antes de montar o componente, verifica se o usuário está logado
onBeforeMount(async () => {
    if (!authStore.isAuthenticated) {
        // Redireciona para a página de login
        router.push({ name: 'login' });
    }

    // Carrega dados do usuário
    await authStore.currentUser();

    user.value = authStore.user;
});


</script>

<script>
export default {
    name: "HomePage",
};
</script>