<template>
  <div v-if="graphs.length" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
    <GraphCard
      v-for="(graph, index) in graphs"
      :key="`graph-${index}`"
      :graph="graph"
      :index="index"
      :deleting-graph-id="deletingGraphId"
      :get-graph-title="getGraphTitle"
      :get-graph-component="getGraphComponent"
      :is-valid-graph-type="isValidGraphType"
      @confirm-delete="$emit('confirmDelete', $arguments[0], $arguments[1])"
    />
  </div>
  
  <!-- Loading State -->
  <div v-else-if="loading" class="flex justify-center items-center min-h-[400px]">
    <div class="text-center">
      <div class="relative">
        <div class="w-16 h-16 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mx-auto mb-4"></div>
        <div class="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-blue-400 rounded-full animate-spin mx-auto" style="animation-delay: -0.15s; animation-duration: 0.8s;"></div>
      </div>
      <p class="text-slate-600 font-medium">Loading your graphs...</p>
      <p class="text-slate-400 text-sm mt-1">Please wait while we fetch your data</p>
    </div>
  </div>
  
  <!-- Empty State -->
  <div v-else class="flex justify-center items-center min-h-[400px]">
    <div class="text-center max-w-md">
      <div class="bg-gradient-to-br from-slate-100 to-slate-200 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
        <BarChart3 class="h-12 w-12 text-slate-400" />
      </div>
      <h3 class="text-2xl font-bold text-slate-700 mb-3">No graphs yet</h3>
      <p class="text-slate-500 leading-relaxed">Create your first graph to get started with beautiful data visualization and analytics</p>
    </div>
  </div>
</template>

<script>
import { BarChart3 } from 'lucide-vue-next'
import GraphCard from './GraphCard.vue'

export default {
  name: 'GraphGrid',
  components: { BarChart3, GraphCard },
  props: {
    graphs: Array,
    loading: Boolean,
    deletingGraphId: String,
    getGraphTitle: Function,
    getGraphComponent: Function,
    isValidGraphType: Function,
  },
  emits: ['confirmDelete'],
}
</script>