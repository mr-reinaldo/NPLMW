const Home = () => import(/* webpackChunkName: "home" */ './../views/Home.vue')

// Rotas filhas
import profileRoutes from './../modules/profile/routes';
import dashboardRoutes from './../modules/dashboard/routes';
import devicesRoutes from './../modules/devices/routes';
import addRoutes from './../modules/add/routes';
import routeRoutes from '../modules/route/routes';


export default [
    {
        path: '/home',
        name: 'home',
        component: Home,
        meta: {
            auth: true
        },
        children:[
            ...profileRoutes,
            ...dashboardRoutes,
            ...devicesRoutes,
            ...routeRoutes,
            ...addRoutes,
            {
                path: '/home',
                redirect: '/home/dashboard'
            }
        ]
    }
]
