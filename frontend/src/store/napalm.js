import {defineStore} from 'pinia'
import {ref} from 'vue'
import http from '@/services/http'

export const useNapalmStore = defineStore('napalm',() => {
    const status = ref(false)
    const message = ref('')
    const data = ref({})
    const timestamp = ref(0)



    const getFacts = async (device) => {

        try{
            const response = await http.post('/facts', device)

            if (response.data.status){
                status.value = response.data.status
                message.value = response.data.message
                data.value = response.data.data
                timestamp.value = response.data.timestamp
            }else{
                throw new Error(response.data.message)
            }
        } catch(error){
            message.value = error.message
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
        message,
        data,
        timestamp,
        getFacts,
        staticRoute,
        Interfaces,
        Ping
    }
})