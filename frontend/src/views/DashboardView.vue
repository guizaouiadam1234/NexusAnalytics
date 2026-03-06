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

        <div v-if="summoner" class="rounded-xl border border-zinc-700 bg-zinc-900/80 p-4">
          <h2 class="text-xl font-semibold text-white">{{ summoner.gameName }}#{{ summoner.tagLine }}</h2>
          <p class="mt-1 text-sm text-zinc-400 break-all">PUUID: {{ summoner.puuid }}</p>
        </div>

        <div v-if="matchCards.length" class="mt-4 space-y-4">
          <div
            v-for="card in matchCards"
            :key="card.matchId"
            class="rounded-xl border border-zinc-700 bg-zinc-900/80 p-4"
          >
            <div class="flex flex-col gap-4 md:flex-row md:items-stretch">
              <div class="w-full md:w-40 rounded-lg border border-zinc-700 bg-zinc-950/70 p-3 flex items-center justify-center">
                <img
                  :src="card.player.championIconUrl"
                  :alt="`${card.player.championName} icon`"
                  class="h-24 w-24 rounded-lg object-cover"
                />
              </div>

              <div class="flex-1 rounded-lg border border-zinc-700 bg-zinc-950/70 p-3">
                <p class="text-xs uppercase tracking-[0.2em] text-zinc-400">
                  {{ card.player.championName }} • {{ card.gameMode }}
                </p>
                <p class="mt-2 text-xl font-semibold text-white">{{ card.player.kda }} KDA</p>
                <p class="mt-1 text-sm text-zinc-300">{{ card.player.cs }} CS • {{ card.player.csPerMinute }} CS/min</p>
                <p class="mt-2 text-xs uppercase tracking-wider" :class="card.player.win ? 'text-emerald-300' : 'text-rose-300'">
                  {{ card.player.win ? 'Victory' : 'Defeat' }}
                </p>
              </div>
            </div>

            <div class="mt-4 grid grid-cols-1 gap-3 md:grid-cols-[1fr_auto_1fr] md:items-stretch">
              <div class="rounded-lg border border-zinc-700 bg-zinc-950/70 p-3">
                <p class="text-xs uppercase tracking-wider text-zinc-400">My Team</p>
                <ul class="mt-2 space-y-1">
                  <li v-for="participant in card.teams.ally" :key="`${card.matchId}-ally-${participant.gameName}-${participant.tagLine}`" class="text-sm text-zinc-200">
                    {{ participant.gameName }}#{{ participant.tagLine }}
                  </li>
                </ul>
              </div>

              <div class="flex items-center justify-center px-2">
                <span class="text-lg font-semibold tracking-widest text-zinc-300">VS</span>
              </div>

              <div class="rounded-lg border border-zinc-700 bg-zinc-950/70 p-3">
                <p class="text-xs uppercase tracking-wider text-zinc-400">Enemy Team</p>
                <ul class="mt-2 space-y-1">
                  <li
                    v-for="participant in card.teams.enemy"
                    :key="`${card.matchId}-enemy-${participant.gameName}-${participant.tagLine}`"
                    class="text-sm text-zinc-200"
                  >
                    {{ participant.gameName }}#{{ participant.tagLine }}
                  </li>
                </ul>
              </div>
            </div>

            <p class="mt-3 text-xs text-zinc-500">
              {{ card.matchId }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

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

    const cardsResponse = await fetchMatchCards(summonerData.puuid, 5)
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
