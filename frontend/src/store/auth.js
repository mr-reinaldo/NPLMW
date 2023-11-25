// Utilities
import {defineStore} from 'pinia'
import {ref} from 'vue'
import http from '@/services/http'


export const useAuthStore = defineStore('auth', () =>{

    // State
    const token = ref(localStorage.getItem('@access_token')) // Token de acesso do usuário
    const type = ref(localStorage.getItem('@token_type')) // Tipo de token do usuário (Bearer)
    const user = ref({}) // Usuário autenticado
    const isAuthenticated = ref(false) // Se o usuário está autenticado ou não

    // Setters
    const setToken = (tokenValue, typeValue) => {
        token.value = tokenValue // Atribui o token de acesso

        // Capitaliza o tipo de token
        typeValue = typeValue.charAt(0).toUpperCase() + typeValue.slice(1)
        type.value = typeValue // Atribui o tipo de token

        localStorage.setItem('@access_token', token.value) // Salva o token de acesso no localStorage
        localStorage.setItem('@token_type', type.value ) // Salva o tipo de token no localStorage
        isAuthenticated.value = true // Define que o usuário está autenticado
    }

    // Actions
    const logout = () => {
        token.value = null // Remove o token de acesso
        type.value = null // Remove o tipo de token
        localStorage.removeItem('@access_token') // Remove o token de acesso do localStorage
        localStorage.removeItem('@token_type') // Remove o tipo de token do localStorage
        isAuthenticated.value = false // Define que o usuário não está autenticado
    }

    const currentUser = async () => {
        const {data} = await http.get('/users/me') // Obtém os dados do usuário autenticado
        user.value = data // Atribui o usuário autenticado
    }


    return {
        token,
        type,
        user,
        isAuthenticated,
        setToken,
        logout,
        currentUser
    }

})