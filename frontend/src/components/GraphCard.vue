<template>
  <div class="group bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20 
              hover:shadow-2xl hover:shadow-purple-500/10 transition-all duration-300 
              hover:scale-[1.02] hover:bg-white"
       :class="{ 'cursor-move': isDraggable }"
       :draggable="isDraggable"
       @dragstart="onDragStart"
       @dragend="onDragEnd">
    <!-- Card Header -->
    <div class="p-6 pb-3">
      <div class="flex justify-between items-start">
        <div class="flex gap-4 flex-1">
          <div class="bg-gradient-to-br from-purple-500 to-purple-600 p-3 rounded-xl shadow-lg">
            <BarChart3 class="h-6 w-6 text-white" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-slate-800 group-hover:text-purple-700 transition-colors truncate">
              {{ getGraphTitle(graph.graph_name) }}
            </h3>
            <div class="flex items-center gap-1 mt-1">
              <Hash class="h-3 w-3 text-slate-400" />
              <span class="text-xs text-slate-500 font-mono">{{ graph.graph_id }}</span>
            </div>
          </div>
        </div>
        <button 
          v-if="!isDraggable"
          @click="$emit('confirmDelete', graph.graph_id, index)"
          class="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg 
                 transition-all duration-200 group-hover:opacity-100 opacity-70"
          :disabled="deletingGraphId === graph.graph_id"
          title="Delete Graph"
        >
          <Trash2 
            class="h-4 w-4"
            :class="{ 'animate-spin': deletingGraphId === graph.graph_id }"
          />
        </button>
        <div v-else class="p-2 text-slate-400">
          <GripVertical class="h-4 w-4" />
        </div>
      </div>
    </div>

    <!-- Graph Content -->
    <div class="px-6 pb-6">
      <div class="bg-gradient-to-br from-slate-50 to-white rounded-xl p-4 min-h-[280px] 
                  flex items-center justify-center border border-slate-100">
        <component
          :is="getGraphComponent(graph.graph_name)"
          :title="getGraphTitle(graph.name)"
          :chartInput="graph.graph_data"
          v-if="isValidGraphType(graph.graph_name)"
        />
        
        <!-- Fallback for unknown graph types -->
        <div v-else class="flex flex-col items-center gap-3 text-slate-500">
          <AlertCircle class="h-8 w-8 text-amber-500" />
          <p class="text-sm font-medium">Unknown Graph Type: {{ graph.graph_name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BarChart3, Hash, Trash2, AlertCircle, GripVertical } from 'lucide-vue-next'
import BarGraph from '@/components/BarGraph.vue'
import PIEChart from '@/components/PIEChart.vue'
import DoughnutChart from '@/components/DoughnutGraph.vue'

export default {
  name: 'GraphCard',
  components: {
    BarChart3, Hash, Trash2, AlertCircle, GripVertical,
    BarGraph, PIEChart, DoughnutChart
  },
  props: {
    graph: Object,
    index: Number,
    deletingGraphId: String,
    getGraphTitle: Function,
    getGraphComponent: Function,
    isValidGraphType: Function,
    isDraggable: { type: Boolean, default: false },
  },
  emits: ['confirmDelete', 'dragStart', 'dragEnd'],
  methods: {
    onDragStart(event) {
      event.dataTransfer.setData('text/plain', JSON.stringify({
        graphId: this.graph.graph_id,
        graphName: this.graph.graph_name,
        graphData: this.graph.graph_data,
        name: this.graph.name
      }))
      this.$emit('dragStart', this.graph)
    },
    onDragEnd() {
      this.$emit('dragEnd')
    }
  }
}
</script>