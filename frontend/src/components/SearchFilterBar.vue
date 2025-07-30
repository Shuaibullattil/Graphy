<template>
  <div class="max-w-7xl mx-auto mb-8">
    <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6">
      <div class="flex flex-col lg:flex-row gap-4">
        <!-- Search Input -->
        <div class="relative flex-1">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Search class="h-5 w-5 text-slate-400" />
          </div>
          <input
            :value="searchQuery"
            @input="onSearchQueryChange($event.target.value)"
            type="text"
            placeholder="Search by graph name..."
            class="w-full pl-11 pr-4 py-3 bg-slate-50/50 border border-slate-200 rounded-xl 
                   focus:ring-2 focus:ring-purple-500 focus:border-transparent 
                   transition-all duration-200 text-slate-700 placeholder-slate-400
                   hover:bg-white/70 focus:bg-white"
          />
          <button
            v-if="searchQuery"
            @click="onSearchQueryChange('')"
            class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
          >
            <X class="h-4 w-4" />
          </button>
        </div>

        <!-- File Name Dropdown -->
        <div class="relative lg:w-64">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Filter class="h-5 w-5 text-slate-400" />
          </div>
          <select
            :value="fileName"
            @change="onFileNameChange($event.target.value)"
            class="w-full pl-11 pr-10 py-3 bg-slate-50/50 border border-slate-200 rounded-xl
                   focus:ring-2 focus:ring-purple-500 focus:border-transparent 
                   transition-all duration-200 text-slate-700 cursor-pointer
                   hover:bg-white/70 focus:bg-white appearance-none"
          >
            <option value="">All Files</option>
            <option v-for="file in fileNames" :key="file.file_id" :value="file.fileName">
              {{ file.fileName }}
            </option>
          </select>
          <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <ChevronDown class="h-4 w-4 text-slate-400" />
          </div>
        </div>

        <!-- Graph Type Dropdown -->
        <div class="relative lg:w-64">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Filter class="h-5 w-5 text-slate-400" />
          </div>
          <select
            :value="selectedType"
            @change="onSelectedTypeChange($event.target.value)"
            class="w-full pl-11 pr-10 py-3 bg-slate-50/50 border border-slate-200 rounded-xl
                   focus:ring-2 focus:ring-purple-500 focus:border-transparent 
                   transition-all duration-200 text-slate-700 cursor-pointer
                   hover:bg-white/70 focus:bg-white appearance-none"
          >
            <option value="">All Graph Types</option>
            <option v-for="type in availableGraphTypes" :key="type" :value="type">
              {{ getGraphTitle(type) }}
            </option>
          </select>
          <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <ChevronDown class="h-4 w-4 text-slate-400" />
          </div>
        </div>

        <!-- Results Count -->
        <div class="flex items-center px-4 py-3 bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl border border-purple-100">
          <span class="text-sm font-medium text-slate-600">
            {{ filteredCount }} {{ filteredCount === 1 ? 'graph' : 'graphs' }}
          </span>
        </div>
      </div>

      <!-- Active Filters -->
      <div v-if="searchQuery || selectedType || fileName" class="mt-4 flex flex-wrap gap-2">
        <span class="text-sm text-slate-500 mr-2">Active filters:</span>
        <span v-if="searchQuery" class="inline-flex items-center gap-1 px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
          Search: "{{ searchQuery }}"
          <button @click="onSearchQueryChange('')" class="hover:text-purple-900">
            <X class="h-3 w-3" />
          </button>
        </span>
        <span v-if="selectedType" class="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
          Type: {{ getGraphTitle(selectedType) }}
          <button @click="onSelectedTypeChange('')" class="hover:text-blue-900">
            <X class="h-3 w-3" />
          </button>
        </span>
        <span v-if="fileName" class="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
          File: {{ fileName }}
          <button @click="onFileNameChange('')" class="hover:text-green-900">
            <X class="h-3 w-3" />
          </button>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { Search, Filter, ChevronDown, X } from 'lucide-vue-next'

export default {
  name: 'SearchFilterBar',
  components: { Search, Filter, ChevronDown, X },
  props: {
    searchQuery: String,
    selectedType: String,
    fileName: String,
    fileNames: Array,
    availableGraphTypes: Array,
    filteredCount: Number,
    getGraphTitle: Function,
  },
  emits: ['update:searchQuery', 'update:selectedType', 'update:fileName', 'search'],
  methods: {
    onSearchQueryChange(val) {
      this.$emit('update:searchQuery', val)
      this.$emit('search', { searchQuery: val, selectedType: this.selectedType, fileName: this.fileName })
    },
    onSelectedTypeChange(val) {
      this.$emit('update:selectedType', val)
      this.$emit('search', { searchQuery: this.searchQuery, selectedType: val, fileName: this.fileName })
    },
    onFileNameChange(val) {
      this.$emit('update:fileName', val)
      this.$emit('search', { searchQuery: this.searchQuery, selectedType: this.selectedType, fileName: val })
    },
  },
}
</script>