const Devices = () => import(/* webpackChunkName: "devices" */ './../views/Devices.vue')

export default [
    {
        path: '/home/devices',
        name: 'devices',
        component: Devices,
        meta: {
            auth: true
        },
    }
]