<template>
  <header class="bg-black/95 border-b border-blue-500/30 shadow-lg shadow-blue-950/40 sticky top-0 z-50 backdrop-blur-sm">
    <div class="container mx-auto px-6 py-4 flex items-center justify-between">

      <!-- Brand -->
      <div class="flex items-center gap-3">
        <div>
          <span class="text-white text-xl font-bold tracking-widest uppercase">Nexus</span>
          <span class="text-blue-400 text-xl font-bold tracking-widest uppercase">Analytics</span>
        </div>
      </div>

      <!-- Nav -->
      <nav class="hidden md:flex items-center gap-8">
        <RouterLink
          v-for="link in navLinks"
          :key="link.label"
          :to="link.to"
          class="text-zinc-400 text-sm font-medium tracking-wider uppercase hover:text-blue-400 transition-colors duration-200 relative group"
        >
          {{ link.label }}
          <span class="absolute -bottom-1 left-0 w-0 h-px bg-blue-400 group-hover:w-full transition-all duration-300"></span>
        </RouterLink>
      </nav>

      <!-- CTA -->
      <div class="hidden md:flex items-center gap-3">
        <button class="text-zinc-400 text-sm font-medium tracking-wider uppercase hover:text-white transition-colors duration-200">
          Sign In
        </button>
        <button class="bg-blue-500 hover:bg-blue-400 text-black text-sm font-bold tracking-wider uppercase px-5 py-2 rounded-sm transition-colors duration-200 shadow-md shadow-blue-500/25">
          Get Started
        </button>
      </div>

      <!-- Mobile menu button -->
      <button
        class="md:hidden text-zinc-400 hover:text-blue-400 transition-colors"
        @click="mobileOpen = !mobileOpen"
      >
        <svg v-if="!mobileOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileOpen" class="md:hidden border-t border-blue-500/25 bg-zinc-950 px-6 py-4 flex flex-col gap-4">
      <RouterLink
        v-for="link in navLinks"
        :key="link.label"
        :to="link.to"
        class="text-zinc-400 text-sm font-medium tracking-wider uppercase hover:text-blue-400 transition-colors duration-200"
        @click="mobileOpen = false"
      >
        {{ link.label }}
      </RouterLink>
      <div class="flex flex-col gap-2 pt-2 border-t border-zinc-800">
        <button class="text-zinc-400 text-sm font-medium tracking-wider uppercase hover:text-white transition-colors text-left">
          Sign In
        </button>
        <button class="bg-blue-500 hover:bg-blue-400 text-black text-sm font-bold tracking-wider uppercase px-5 py-2 rounded-sm transition-colors duration-200 w-full">
          Get Started
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const mobileOpen = ref(false)

const navLinks = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Analytics', to: '/analytics' },
  { label: 'Reports', to: '/reports' },
  { label: 'Docs', to: '/docs' },
]
</script>