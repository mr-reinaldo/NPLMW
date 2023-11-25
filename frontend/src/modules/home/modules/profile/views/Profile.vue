<template>
    <v-row>
        <v-col cols="12">
            <v-card flat elevation="0" rounded="0">
                <v-toolbar color="primary">
                    <v-toolbar-title>Meu Perfil</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn :prepend-icon="isEditing ? 'mdi-close' : 'mdi-pencil'" text @click="isEditing = !isEditing"
                        :color="isEditing ? 'red' : 'white'" variant="flat">
                        {{ isEditing ? 'Cancelar' : 'Editar' }}
                    </v-btn>
                </v-toolbar>
                <v-card-text class="py-8 mb-8">
                    <!--Foto do Usuário Centralizada-->
                    <v-row justify="center" class="mb-6">
                        <v-avatar size="200" variant="plain">
                            <v-img src="@/assets/user.svg"></v-img>
                        </v-avatar>
                    </v-row>
                    <!--Formulário-->
                    <v-row justify="center">
                        <v-col cols="12" md="6">
                            <v-form :disabled="!isEditing">
                                <v-text-field label="Nome de usuário" prepend-icon="mdi-account" v-model="username"
                                    variant="outlined" density="comfortable" required></v-text-field>
                                <v-text-field label="E-mail" prepend-icon="mdi-email" v-model="email" variant="outlined"
                                    density="comfortable" required></v-text-field>
                                <v-text-field label="Senha" prepend-icon="mdi-lock" v-model="password" variant="outlined"
                                    density="comfortable" :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                    :type="showPassword ? 'text' : 'password'"
                                    @click:append-inner="showPassword = !showPassword"></v-text-field>
                            </v-form>
                        </v-col>
                    </v-row>
                </v-card-text>

                <v-snackbar v-model="state.showSnackbar" multi-line location="top">
                    {{ state.detail }}

                    <template v-slot:actions>
                        <v-btn color="red" variant="text" @click="state.showSnackbar = false">
                            Fechar
                        </v-btn>
                    </template>
                </v-snackbar>

                <v-card-actions class="mb-12">
                    <v-spacer></v-spacer>
                    <v-btn color="primary" prepend-icon="mdi-content-save" :disabled="!isEditing" @click="updateUser"
                        :loading="isLoading" variant="flat">
                        Salvar Alterações
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</template>

<script setup>

import { ref, watchEffect } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useUserStore } from '@/store/user';

const showPassword = ref(false)
const isEditing = ref(false)

const authStore = useAuthStore()
const userStore = useUserStore()

const username = ref('')
const email = ref('')
const password = ref('')

const isLoading = ref(false)

const state = ref({
    showSnackbar: false,
    detail: ''
})

// Carregar dados do usuário
watchEffect( async () => {
    await userStore.getUser(authStore.user.uuid)

    username.value = userStore.user.username
    email.value = userStore.user.email
    password.value = userStore.user.password
})


// Atualizar usuário
const updateUser = () => {
    try {
        isLoading.value = true

        const user = {
            username: username.value,
            email: email.value,
            password: password.value
        }
        userStore.updateUser(authStore.user.uuid,user)
        isLoading.value = false
        isEditing.value = false
        state.value.showSnackbar = true
        state.value.detail = 'Usuário atualizado com sucesso!'
    } catch (error) {
        isLoading.value = false
        state.value.showSnackbar = true
        state.value.detail = error.response.data.detail
    }finally{
        isLoading.value = false
    }
}


</script>


<script>
export default {
    name: 'ProfilePage',
}
</script>