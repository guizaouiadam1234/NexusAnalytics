<template>
  <div class="rounded-xl border border-zinc-700 bg-zinc-900/80 p-4">
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
          <li
            v-for="participant in card.teams.ally"
            :key="`${card.matchId}-ally-${participant.gameName}-${participant.tagLine}`"
            class="flex items-center gap-2 text-sm text-zinc-200"
          >
            <img
              :src="participant.championIconUrl"
              :alt="`${participant.championName} icon`"
              class="h-5 w-5 rounded-sm object-cover"
            />
            <span>{{ participant.gameName }}#{{ participant.tagLine }}</span>
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
            class="flex items-center gap-2 text-sm text-zinc-200"
          >
            <img
              :src="participant.championIconUrl"
              :alt="`${participant.championName} icon`"
              class="h-5 w-5 rounded-sm object-cover"
            />
            <span>{{ participant.gameName }}#{{ participant.tagLine }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  card: {
    type: Object,
    required: true,
  },
})
</script>
