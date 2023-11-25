import { defineStore } from 'pinia';
import { ref } from 'vue';
import http from '@/services/http';


export const useUserStore = defineStore('user', () => {

    // State
    const user = ref(null)

    // Actions
    const getUser = async (uuid) => {
        const { data } = await http.get(`/users/${uuid}`)
        user.value = data
    }

    const createUser = async (data) => {
        await http.post('/users/signup', data)
    }

    const updateUser = async (uuid, data) => {
        await http.put(`/users/${uuid}`, data)
    }

    const deleteUser = async (uuid) => {
        await http.delete(`/users/${uuid}`)
    }

    return {
        user,
        getUser,
        createUser,
        updateUser,
        deleteUser
    }
})