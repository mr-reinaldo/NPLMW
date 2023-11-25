<template>
    <!--Card recebe a quantidade total de dispositivos cadastrados, cor do card-->
    <v-card class="elevation-2" :color="props.color" width="100%" height="100%">
        <v-card-title class="text-h6">
            <v-icon>mdi-{{ props.icon }}</v-icon>
            {{ title }}
        </v-card-title>
        <v-card-text >
            <v-row align="center" justify="center">
                <v-col cols="12" class="text-center mt-4">
                    <span class="text-h3">{{ props.total }}</span>
                </v-col>
            </v-row>

        </v-card-text>
    </v-card>
</template>

<script setup>
    import { ref, defineProps } from 'vue';

    const props = defineProps({
        title: String,
        total: Number,
        icon: String,
        color: String,
    })

    const title = ref(props.title);
    const total = ref(props.total);
    const icon = ref(props.icon);
    const color = ref(props.color);
    






</script>

<script>
    export default {
        name: 'CardInformation',
    }
</script>
