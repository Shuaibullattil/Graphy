<template>
  <div class="max-w-7xl mx-auto">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[calc(100vh-200px)]">
      <!-- Left Side - Available Graphs -->
      <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 overflow-hidden flex flex-col">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold text-slate-800">Available Graphs</h2>
          <span class="text-sm text-slate-500">{{ availableGraphs.length }} graphs</span>
        </div>

        <!-- Search and Filter for available graphs -->
        <SearchFilterBar
          v-model:search-query="searchQuery"
          v-model:selected-type="selectedType"
          :available-graph-types="availableGraphTypes"
          :filtered-count="filteredAvailableGraphs.length"
          :get-graph-title="getGraphTitle"
        />

        <!-- Available Graphs List -->
        <div class="flex-1 overflow-y-auto">
          <div class="grid gap-4">
            <GraphCard
              v-for="(graph, index) in filteredAvailableGraphs"
              :key="`available-${graph.graph_id}`"
              :graph="graph"
              :index="index"
              :get-graph-title="getGraphTitle"
              :get-graph-component="getGraphComponent"
              :is-valid-graph-type="isValidGraphType"
              :is-draggable="true"
              @drag-start="onDragStart"
            />
          </div>
          
          <div v-if="filteredAvailableGraphs.length === 0" class="text-center py-12 text-slate-500">
            <BarChart3 class="h-12 w-12 mx-auto mb-4 text-slate-300" />
            <p>No available graphs found</p>
          </div>
        </div>
      </div>

      <!-- Right Side - Dashboard Builder -->
      <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 overflow-hidden flex flex-col">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-slate-800 mb-4">Create Dashboard</h2>
          
          <!-- Dashboard Name Input -->
          <input
            v-model="dashboardName"
            type="text"
            placeholder="Enter dashboard name..."
            class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl 
                   focus:ring-2 focus:ring-purple-500 focus:border-transparent 
                   transition-all duration-200 text-slate-700 placeholder-slate-400"
          />
        </div>

        <!-- Drop Zone -->
        <div
          class="flex-1 border-2 border-dashed border-slate-300 rounded-xl p-6 
                 transition-all duration-200"
          :class="{
            'border-purple-400 bg-purple-50': isDragOver,
            'border-slate-300 bg-slate-50': !isDragOver
          }"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="onDrop"
        >
          <div v-if="selectedGraphs.length === 0" class="h-full flex items-center justify-center text-center">
            <div>
              <Layout class="h-16 w-16 mx-auto mb-4 text-slate-300" />
              <p class="text-slate-500 text-lg font-medium mb-2">Drop graphs here</p>
              <p class="text-slate-400 text-sm">Drag and drop graphs from the left panel to build your dashboard</p>
            </div>
          </div>

          <!-- Selected Graphs Grid -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 h-full overflow-y-auto">
            <div
              v-for="(graph, index) in selectedGraphs"
              :key="`selected-${graph.graph_id}-${index}`"
              class="bg-white rounded-xl p-4 shadow-sm border border-slate-200 relative group"
            >
              <button
                @click="removeGraph(index)"
                class="absolute top-2 right-2 p-1 bg-red-100 text-red-600 rounded-lg 
                       opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-200"
              >
                <X class="h-4 w-4" />
              </button>
              
              <div class="text-center">
                <div class="bg-gradient-to-br from-purple-500 to-purple-600 p-2 rounded-lg inline-flex mb-2">
                  <BarChart3 class="h-4 w-4 text-white" />
                </div>
                <h4 class="text-sm font-medium text-slate-700 truncate">
                  {{ getGraphTitle(graph.graph_name) }}
                </h4>
                <p class="text-xs text-slate-500 font-mono mt-1">{{ graph.graph_id }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-6 flex gap-3">
          <button
            @click="$emit('close')"
            class="flex-1 px-4 py-3 bg-slate-100 text-slate-700 rounded-xl font-medium 
                   hover:bg-slate-200 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="createDashboard"
            :disabled="!canCreateDashboard || isCreating"
            class="flex-1 px-4 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white 
                   rounded-xl font-medium hover:from-purple-600 hover:to-purple-700 
                   transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                   flex items-center justify-center gap-2"
          >
            <div v-if="isCreating" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            <Plus v-else class="h-4 w-4" />
            {{ isCreating ? 'Creating...' : 'Create Dashboard' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import axios from 'axios'
import { BarChart3, Layout, X, Plus } from 'lucide-vue-next'
import SearchFilterBar from './SearchFilterBar.vue'
import GraphCard from './GraphCard.vue'

export default {
  name: 'DashboardCreator',
  components: { BarChart3, Layout, X, Plus, SearchFilterBar, GraphCard },
  props: {
    graphsData: Array,
    availableGraphTypes: Array,
    getGraphTitle: Function,
    getGraphComponent: Function,
    isValidGraphType: Function,
  },
  emits: ['close', 'dashboardCreated'],
  setup(props, { emit }) {
    const dashboardName = ref('')
    const selectedGraphs = ref([])
    const isDragOver = ref(false)
    const isCreating = ref(false)
    
    // Search and filter for available graphs
    const searchQuery = ref('')
    const selectedType = ref('')

    const availableGraphs = computed(() => {
      return props.graphsData.filter(graph => 
        !selectedGraphs.value.some(selected => selected.graph_id === graph.graph_id)
      )
    })

    const filteredAvailableGraphs = computed(() => {
      return availableGraphs.value.filter(graph => {
        const matchesType = selectedType.value ? graph.graph_name === selectedType.value : true
        const matchesSearch = graph.name
          ? graph.name.toLowerCase().includes(searchQuery.value.toLowerCase())
          : false
        return matchesType && matchesSearch
      })
    })

    const canCreateDashboard = computed(() => {
      return dashboardName.value.trim() && selectedGraphs.value.length > 0
    })

    const onDragStart = (graph) => {
      // Handle drag start if needed
    }

    const onDrop = (event) => {
      isDragOver.value = false
      try {
        const graphData = JSON.parse(event.dataTransfer.getData('text/plain'))
        
        // Check if graph is already selected
        if (!selectedGraphs.value.some(graph => graph.graph_id === graphData.graphId)) {
          selectedGraphs.value.push({
            graph_id: graphData.graphId,
            graph_name: graphData.graphName,
            graph_data: graphData.graphData,
            name: graphData.name
          })
        }
      } catch (error) {
        console.error('Error parsing dropped data:', error)
      }
    }

    const removeGraph = (index) => {
      selectedGraphs.value.splice(index, 1)
    }

    const createDashboard = async () => {
      if (!canCreateDashboard.value) return

      isCreating.value = true
      try {
        const token = sessionStorage.getItem('authToken')
        const baseUrl = 'http://localhost:8000'
        
        const response = await axios.post(`${baseUrl}/dashboard/create`, {
          name: dashboardName.value.trim(),
          graphs: selectedGraphs.value.map(graph => graph.graph_id)
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        console.log('Dashboard created successfully:', response.data)
        emit('dashboardCreated', response.data)
        
        // Reset form
        dashboardName.value = ''
        selectedGraphs.value = []
        
      } catch (error) {
        console.error('Error creating dashboard:', error)
        alert('Failed to create dashboard. Please try again.')
      } finally {
        isCreating.value = false
      }
    }

    return {
      dashboardName,
      selectedGraphs,
      isDragOver,
      isCreating,
      searchQuery,
      selectedType,
      availableGraphs,
      filteredAvailableGraphs,
      canCreateDashboard,
      onDragStart,
      onDrop,
      removeGraph,
      createDashboard,
    }
  }
}
</script>