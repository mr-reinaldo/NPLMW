const Route = () => import(/* webpackChunkName: "router" */ './../views/Route.vue');
const Interfaces = () => import(/* webpackChunkName: "router" */ './../views/Interfaces.vue');
const OSPF = () => import(/* webpackChunkName: "router" */ './../views/OSPF.vue');
const StaticRoutes = () => import(/* webpackChunkName: "router" */ './../views/StaticRoutes.vue');

export default [
    {
        path: '/home/route',
        name: 'route',
        component: Route,
        meta: {
            auth: true
        },
        redirect: { name: 'static-routes' },
        children: [
            {
                path: 'interfaces',
                name: 'interfaces',
                component: Interfaces,
                meta: {
                    auth: true
                }
            },
            {
                path: 'ospf',
                name: 'ospf',
                component: OSPF,
                meta: {
                    auth: true
                }
            },
            {
                path: 'static-routes',
                name: 'static-routes',
                component: StaticRoutes,
                meta: {
                    auth: true
                }
            }
        ]
    }
]
