// Utilities
import { defineStore } from 'pinia'

import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () =>{

    const theme = ref(localStorage.getItem('@theme') || 'light')

    const toggleTheme = () => {
        if(theme.value === 'light'){
            theme.value = 'dark'
            localStorage.setItem('@theme', 'dark')
        }else{
            theme.value = 'light'
            localStorage.setItem('@theme', 'light')
        }
    }


    return {
        toggleTheme,
        theme
    }
})