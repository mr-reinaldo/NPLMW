const Login = () => import(/* webpackChunkName: "login" */ './../views/Login.vue');

const routes = [
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
];

export default routes;