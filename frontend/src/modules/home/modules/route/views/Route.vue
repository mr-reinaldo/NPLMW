<template>
    <v-row>
        <v-col cols="12">
            <v-card>
                <v-card-title>
                    <v-tabs v-model="tab" background-color="primary" dark slider-color="secondary">
                        <v-tab v-for="tab in tabsList" :key="tab.key" :to="'/home/route/' + tab.key">
                            <v-icon>{{ tab.icon }}</v-icon>
                            {{ tab.title }}
                        </v-tab>
                    </v-tabs>
                </v-card-title>

                <v-card-text>
                    <router-view></router-view>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref } from 'vue'


const tab = ref(null)

const tabsList = [
    { title: 'Rotas Estáticas', icon: 'mdi-vector-line', key: 'static-routes' },
    { title: 'Interfaces', icon: 'mdi-vector-square', key: 'interfaces' },
    { title: 'OSPF', icon: 'mdi-vector-triangle', key: 'ospf' },
]


</script>

<script>
export default {
    name: 'RoutePage',
}
</script>