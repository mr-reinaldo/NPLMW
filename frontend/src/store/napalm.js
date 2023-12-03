import {defineStore} from 'pinia'
import {ref} from 'vue'
import http from '@/services/http'

export const useNapalmStore = defineStore('napalm',() => {
    const status = ref(0)
    const messageSucesso = ref('')
    const messageFalha = ref('')
    const data = ref({})
    const timestamp = ref(0)



    const getFacts = async (device) => {

        try{
            const response = await http.post('/facts', device)

            // Se status for 200, seta o valor de status para 200
            // e o valor de data para o valor de data que veio da api
            if(response.status === 200){
                status.value = response.status
                messageSucesso.value = response.data.message
                data.value = response.data
                timestamp.value = response.data.timestamp
            }

        } catch(error){
            // Se status for 500, seta o valor de status para 500
            // e o valor de message para o valor de message que veio da api
            if(error.response.status === 500){
                // Zera o valor de data
                data.value = {}
                
                status.value = error.response.status
                messageFalha.value = error.response.data.detail
            }
        }
    }

    const staticRoute = async (request) => {
        try{
            const response = await http.post('/static-routes', request)

            data.value = response.data

        } catch(error){
            console.log('catch-napalm', error.message)
        }
    }

    const Interfaces = async (request) => {
        try{
            const response = await http.post('/interfaces', request)

            data.value = response.data

        } catch(error){
            console.log('catch-napalm', error.message)
        }
    }

    const Ping = async (request) => {
        try{
            const response = await http.post('/ping/ping', request)

            data.value = response.data

        } catch(error){
            console.log('catch-napalm', error.message)
        }
    }

    return {
        status,
        messageSucesso,
        messageFalha,
        data,
        timestamp,
        getFacts,
        staticRoute,
        Interfaces,
        Ping
    }
})