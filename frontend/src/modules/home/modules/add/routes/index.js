const Add = () => import(/* webpackChunkName: "devices" */ '../views/Add.vue')

export default [
    {
        path: '/home/devices/add',
        name: 'add',
        component: Add,
        meta: {
            auth: true
        }
    }
]