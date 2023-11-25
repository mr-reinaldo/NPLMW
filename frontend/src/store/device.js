import {defineStore} from 'pinia'
import {ref} from 'vue'
import http from '@/services/http'

export const useDeviceStore = defineStore('devices',() => {
    const devices = ref([])
    const device = ref({})
    const hostnames = ref({})
    const names = ref([])

    const getDevices = async () => {
        const { data } = await http.get('/devices')
        devices.value = data
    }

    const getDeviceNames = async () => {
        await getDevices()

        devices.value.forEach((device) => {
            if (!names.value.includes(device.name)) {
                names.value.push(device.name)
            }
        })
    }


    const getHostnames = async () => {

        await getDevices()
        
        devices.value.forEach((device) => {
            if (!hostnames.value.includes(device.hostname)) {
                hostnames.value.push(device.hostname)
            }
        })

        return hostnames.value
    }

    const getDevice = async (uuid) => {
        device.value = await http.get(`/devices/${uuid}`)
    }

    const createDevice = async (data) => {
        await http.post('/devices', data)
    }

    const updateDevice = async (uuid, data) => {
        await http.put(`/devices/${uuid}`, data)
    }

    const deleteDevice = async (uuid) => {
        await http.delete(`/devices/${uuid}`)
    }

    return {
        devices,
        device,
        hostnames,
        getDevices,
        getDevice,
        getHostnames,
        createDevice,
        updateDevice,
        deleteDevice,
        getDeviceNames,
    }
})