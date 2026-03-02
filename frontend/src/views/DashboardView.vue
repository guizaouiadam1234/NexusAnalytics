<template>
  <section class="min-h-[70vh] flex items-center flex flex-col justify-between
 px-4">
    <div class="w-full max-w-6xl">
      <div class="mb-6 text-center">
        <h1 class="text-4xl font-bold tracking-tight text-white">Summoner Lookup</h1>
        <p class="mt-2 text-zinc-400">Search by Riot ID in one clean bar.</p>
      </div>

      <form class="rounded-2xl border border-blue-500/25 bg-zinc-900/95 p-3 shadow-2xl shadow-blue-950/30 backdrop-blur-sm">
        <div class="grid grid-cols-1 gap-3 md:grid-cols-[170px_minmax(0,1fr)_210px_70px] md:items-stretch">
          <div class="h-20 rounded-xl border border-zinc-600/80 bg-zinc-800/80 px-4 py-3 flex flex-col justify-between
">
            <label for="region" class="block text-[11px] uppercase tracking-[0.18em] text-zinc-400">Region</label>
            <select
              id="region"
              class="mt-1 w-full bg-transparent text-base font-medium text-zinc-100 outline-none"
            >
              <option value="euw1" class="bg-zinc-900">Europe West</option>
              <option value="eun1" class="bg-zinc-900">Europe Nordic & East</option>
              <option value="na1" class="bg-zinc-900">North America</option>
              <option value="kr" class="bg-zinc-900">Korea</option>
            </select>
          </div>

          <div class="h-20 rounded-xl border border-zinc-600/80 bg-zinc-800/80 px-4 py-3 flex flex-col justify-between
">
            <label for="summoner-name" class="block text-[11px] uppercase tracking-[0.18em] text-zinc-400">Summoner Name</label>
            <input
              id="summoner-name"
              type="text"
              placeholder="e.g. Faker"
              class="mt-1 w-full bg-transparent text-lg font-medium text-zinc-100 placeholder:text-zinc-500 outline-none"
            />
          </div>

          <div class="h-20 rounded-xl border border-zinc-600/80 bg-zinc-800/80 px-4 py-3 flex flex-col justify-between
">
            <label for="summoner-tag" class="block text-[11px] uppercase tracking-[0.18em] text-zinc-400">Summoner Tag</label>
            <div class="mt-1 flex items-center gap-2">
              <span class="text-zinc-500 text-lg font-semibold">#</span>
              <input
                id="summoner-tag"
                type="text"
                placeholder="EUW"
                class="w-full bg-transparent text-lg font-medium text-zinc-100 placeholder:text-zinc-500 outline-none"
              />
            </div>
          </div>

          <button
            type="button"
            class="h-20 rounded-xl bg-blue-500 text-black font-bold text-xl transition-colors duration-200 hover:bg-blue-400 shadow-lg shadow-blue-500/30"
            aria-label="Search summoner"
          >
            Go
          </button>
        </div>
      </form>
    </div>
  </section>
</template>
