<template>
  <section class="px-4 py-8">
    <div class="w-full max-w-6xl mx-auto">
      <div class="mb-6 text-center">
        <h1 class="text-4xl font-bold tracking-tight text-white">Summoner Lookup</h1>
        <p class="mt-2 text-zinc-400">Search by Riot ID in one clean bar.</p>
      </div>

      <form
        class="max-w-5xl mx-auto rounded-2xl border border-blue-600/30 bg-zinc-900/95 p-3 shadow-2xl shadow-blue-950/30 backdrop-blur-sm"
        @submit.prevent="handleSearch"
      >
        <div class="overflow-x-auto">
          <div class="min-w-[980px] h-20 flex items-stretch rounded-xl border border-blue-700/50 bg-blue-900/40 mx-auto">
            <div class="w-56 px-4 py-3 flex flex-col justify-center border-r border-blue-700/60 bg-blue-700/70">
              <label for="region" class="text-[11px] uppercase tracking-[0.18em] text-blue-100">Region</label>
              <select
                id="region"
                v-model="region"
                class="mt-1 w-full appearance-none rounded-md bg-blue-700/90 px-2 py-1 text-base font-semibold text-white outline-none"
              >
                <option value="euw1" class="bg-blue-900">Europe West</option>
                <option value="eun1" class="bg-blue-900">Europe Nordic & East</option>
                <option value="na1" class="bg-blue-900">North America</option>
                <option value="kr" class="bg-blue-900">Korea</option>
              </select>
            </div>

            <div class="flex-1 px-4 py-3 flex flex-col justify-center border-r border-blue-700/60 bg-blue-700/70">
              <label for="summoner-name" class="text-[11px] uppercase tracking-[0.18em] text-blue-100">Summoner Name</label>
              <input
                id="summoner-name"
                v-model="summonerName"
                type="text"
                placeholder="e.g. Faker"
                class="mt-1 w-full rounded-md bg-blue-700/90 px-2 py-1 text-lg font-semibold text-white placeholder:text-blue-100/80 outline-none"
                required
              />
            </div>

            <div class="w-64 px-4 py-3 flex flex-col justify-center border-r border-blue-700/60 bg-blue-700/70">
              <label for="summoner-tag" class="text-[11px] uppercase tracking-[0.18em] text-blue-100">Summoner Tag</label>
              <div class="mt-1 flex items-center gap-2">
                <span class="text-blue-100 text-lg font-semibold">#</span>
                <input
                  id="summoner-tag"
                  v-model="tag"
                  type="text"
                  placeholder="EUW"
                  class="w-full rounded-md bg-blue-700/90 px-2 py-1 text-lg font-semibold text-white placeholder:text-blue-100/80 outline-none"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              class="w-36 bg-blue-600 hover:bg-blue-500 text-black text-sm font-bold tracking-wider uppercase transition-colors duration-200 shadow-md shadow-blue-700/25"
              aria-label="Search summoner"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Loading...' : 'Go' }}
            </button>
          </div>
        </div>
      </form>

      <div class="mt-6 max-w-5xl mx-auto">
        <p v-if="errorMessage" class="rounded-lg border border-red-500/40 bg-red-900/20 px-4 py-3 text-red-200">
          {{ errorMessage }}
        </p>

        <SummonerCard v-if="summoner" :summoner="summoner" />

        <div v-if="matchCards.length" class="mt-4 space-y-4">
          <MatchCard v-for="card in matchCards" :key="card.matchId" :card="card" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

import MatchCard from '@/components/matches/MatchCard.vue'
import SummonerCard from '@/components/matches/SummonerCard.vue'
import { fetchMatchCards, fetchSummoner } from '@/services/api'

const region = ref('euw1')
const summonerName = ref('')
const tag = ref('')

const isLoading = ref(false)
const errorMessage = ref('')

const summoner = ref(null)
const matchCards = ref([])

async function handleSearch() {
  isLoading.value = true
  errorMessage.value = ''
  matchCards.value = []

  try {
    const normalizedTag = tag.value.trim().toUpperCase()
    const summonerData = await fetchSummoner(summonerName.value.trim(), normalizedTag)
    summoner.value = summonerData

    const cardsResponse = await fetchMatchCards(summonerData.puuid, 20)
    matchCards.value = cardsResponse.cards || []
  } catch (error) {
    summoner.value = null
    matchCards.value = []
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load data'
  } finally {
    isLoading.value = false
  }
}
</script>
