import axios from 'axios'

import router from '@/router'

import { useAuthStore } from '@/store/auth'

const axiosInstance = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

axiosInstance.interceptors.request.use(
    config => {
        const useAuth = useAuthStore()
        const token = useAuth.token
        const type = useAuth.type
    

        if (token) {
            config.headers.Authorization = `${type} ${token}`
        }

        return config
    },
    error => {
        return Promise.reject(error)
    }
)

axiosInstance.interceptors.response.use(
    response => {
        return response
    },
    error => {
        if (error.response.status === 401) {
            router.push({ name: 'login' })
        }
        return Promise.reject(error)
    }
)

export default axiosInstance