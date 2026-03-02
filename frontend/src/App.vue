<script setup>
import Header from './components/home/Header.vue'
import { RouterView } from 'vue-router'
</script>

<template>
    <div class="min-h-screen bg-black text-zinc-100">
        <Header />
        <main class="container mx-auto px-6 py-8">
            <RouterView />
        </main>
    </div>
</template>
