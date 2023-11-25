const Profile = () => import(/* webpackChunkName: "profile" */ './../views/Profile.vue')

export default [
    {
        path: '/home/profile',
        name: 'profile',
        component: Profile,
        meta: {
            auth: true
        }
    }
]