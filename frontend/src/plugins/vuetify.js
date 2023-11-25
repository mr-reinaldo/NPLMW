/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#26A69A',
          secondary: '#5CBBF6',
          background: '#ECEFF0', //#CFD8DC
        },
      },
      dark: {
        colors: {
          primary: '#00897B',
          secondary: '#5CBBF6',
        },
      },
    },
  },
})
