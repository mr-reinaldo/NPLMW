const Dashboard = () => import(/* webpackChunkName: "dashboard" */ './../views/Dashboard.vue')

export default [
    {
        path: '/home/dashboard',
        name: 'dashboard',
        component: Dashboard,
        meta: {
            auth: true
        }
    }
]