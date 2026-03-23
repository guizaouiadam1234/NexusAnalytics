<template>
  <div class="rounded-xl border border-zinc-700 bg-zinc-900/80 p-4">
    <h2 class="text-xl font-semibold text-white">{{ summoner.gameName }}#{{ summoner.tagLine }}</h2>
  </div>
</template>

<script setup>
defineProps({
  summoner: {
    type: Object,
    required: true,
  },
})
</script>
