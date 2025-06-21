<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-4 md:p-6">
    
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-blue-600" />
      <span class="ml-2 text-gray-600">Loading dashboards...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div class="flex items-center gap-2">
        <AlertCircle class="w-5 h-5 text-red-500" />
        <span class="text-red-700">{{ error }}</span>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Dashboard Selection Bubbles -->
      <div class="mb-8">
        <h2 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <Layers class="w-5 h-5" />
          Select Dashboard
        </h2>
        <div class="flex flex-wrap gap-3">
          <div
            v-for="dashboard in dashboards"
            :key="dashboard.dashboard_id"
            @click="selectDashboard(dashboard)"
            :class="[
              'px-6 py-3 bg-white rounded-full shadow-md hover:shadow-lg transition-all duration-200 cursor-pointer border-2',
              selectedDashboard?.dashboard_id === dashboard.dashboard_id
                ? 'border-blue-500 bg-blue-50 text-blue-700 shadow-blue-100'
                : 'border-transparent hover:border-blue-200 text-gray-700'
            ]"
          >
            <div class="flex items-center gap-2">
              <TrendingUp class="w-4 h-4" />
              <span class="font-medium">{{ dashboard.name }}</span>
              <span v-if="dashboard.graphs?.length" 
                    class="text-xs bg-gray-100 px-2 py-1 rounded-full">
                {{ dashboard.graphs.length }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Graphs Loading -->
      <div v-if="graphsLoading" class="flex items-center justify-center py-12">
        <Loader2 class="w-6 h-6 animate-spin text-blue-600" />
        <span class="ml-2 text-gray-600">Loading graphs...</span>
      </div>

      <!-- No Dashboard Selected -->
      <div v-else-if="!selectedDashboard" class="text-center py-16">
        <MousePointerClick class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-xl font-medium text-gray-500 mb-2">Select a Dashboard</h3>
        <p class="text-gray-400">Choose a dashboard above to view its graphs and analytics</p>
      </div>

      <!-- No Graphs Available -->
      <div v-else-if="dashboardGraphs.length === 0" class="text-center py-16">
        <ChartNoAxesColumn class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-xl font-medium text-gray-500 mb-2">No Graphs Available</h3>
        <p class="text-gray-400">This dashboard doesn't have any graphs yet</p>
      </div>

      <!-- Graphs Grid -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <div
          v-for="graph in dashboardGraphs"
          :key="graph.graph_id"
          class="bg-white rounded-xl shadow-sm border hover:shadow-md transition-shadow duration-200"
        >
          <div class="p-6">
            <!-- Graph Header -->
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <component :is="getGraphIcon(graph.graph_type)" class="w-5 h-5 text-blue-600" />
                {{ graph.name }}
              </h4>
              <div class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                {{ getGraphTitle(graph.graph_type) }}
              </div>
            </div>

            <!-- Graph Component -->
            <div class="min-h-[300px] flex items-center justify-center">
              <component
                :is="getGraphComponent(graph.graph_type)"
                :title="graph.name"
                :chartInput="graph.data"
                :labels="graph.labels"
                v-if="isValidGraphType(graph.graph_type)"
                class="w-full h-full"
              />
              <div v-else class="text-center py-8">
                <AlertTriangle class="w-8 h-8 text-yellow-500 mx-auto mb-2" />
                <p class="text-gray-500">Unsupported graph type: {{ graph.graph_type }}</p>
              </div>
            </div>

            <!-- Graph Footer -->
            <div class="mt-4 pt-4 border-t border-gray-100">
              <div class="flex items-center justify-between text-sm text-gray-500">
                <span>{{ graph.data?.length || 0 }} data points</span>
                <span class="font-mono">ID: {{ graph.graph_id.slice(-8) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PIEChart from '@/components/PieChart.vue';
import BarGraph from '@/components/BarGraph.vue';
import DoughnutGraph from '@/components/DoughnutGraph.vue';
import { 
  LayoutDashboard, 
  Layers, 
  TrendingUp, 
  BarChart3, 
  MousePointerClick, 
  ChartNoAxesColumn,
  Loader2, 
  AlertCircle, 
  AlertTriangle,
  PieChart,
  BarChart2
} from 'lucide-vue-next';

export default {
  name: "Mydashboards",
  components: {
    PIEChart,
    BarGraph,
    DoughnutGraph,
    LayoutDashboard,
    Layers,
    TrendingUp,
    BarChart3,
    MousePointerClick,
    ChartNoAxesColumn,
    Loader2,
    AlertCircle,
    AlertTriangle,
    PieChart,
    BarChart2
  },
  data() {
    return {
      dashboards: [],
      selectedDashboard: null,
      dashboardGraphs: [],
      loading: true,
      graphsLoading: false,
      error: null,
      baseUrl: '', // Will be set in mounted()
      graphConfig: {
        '001': {
          component: 'BarGraph',
          title: 'Bar Chart',
          icon: 'BarChart2'
        },
        '002': {
          component: 'PIEChart',
          title: 'Pie Chart',
          icon: 'PieChart'
        },
        '003': {
          component: 'DoughnutGraph',
          title: 'Doughnut Chart',
          icon: 'PieChart'
        }
      }
    };
  },
  async mounted() {
    // Set base URL - you can configure this in multiple ways:
    this.baseUrl = this.getBaseUrl();
    await this.fetchDashboards();
  },
  methods: {
    getBaseUrl() {
      // Best practice: Use Vue global config
      return this.$config?.apiBaseUrl || 'http://localhost:3000';
    },

    getAuthHeaders() {
      const authToken = sessionStorage.getItem('authToken');
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }
      
      return headers;
    },
    async fetchDashboards() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await fetch(`${this.baseUrl}/dashboard/about`, {
          headers: this.getAuthHeaders()
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Authentication failed. Please login again.');
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.dashboard && Array.isArray(data.dashboard)) {
          this.dashboards = data.dashboard;
          
          // Auto-select first dashboard if available
          if (this.dashboards.length > 0) {
            await this.selectDashboard(this.dashboards[0]);
          }
        } else {
          throw new Error('Invalid response format');
        }
      } catch (err) {
        console.error('Error fetching dashboards:', err);
        this.error = `Failed to load dashboards: ${err.message}`;
      } finally {
        this.loading = false;
      }
    },

    async selectDashboard(dashboard) {
      if (this.selectedDashboard?.dashboard_id === dashboard.dashboard_id) {
        return; // Already selected
      }

      try {
        this.selectedDashboard = dashboard;
        this.graphsLoading = true;
        this.dashboardGraphs = [];
        
        const response = await fetch(`${this.baseUrl}/dashboard/my/${dashboard.dashboard_id}`, {
          headers: this.getAuthHeaders()
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Authentication failed. Please login again.');
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.graphs && Array.isArray(data.graphs)) {
          this.dashboardGraphs = data.graphs;
        } else {
          this.dashboardGraphs = [];
        }
      } catch (err) {
        console.error('Error fetching dashboard graphs:', err);
        this.error = `Failed to load graphs: ${err.message}`;
        this.dashboardGraphs = [];
      } finally {
        this.graphsLoading = false;
      }
    },

    getGraphComponent(graphType) {
      const config = this.graphConfig[graphType];
      return config ? config.component : null;
    },

    getGraphTitle(graphType) {
      const config = this.graphConfig[graphType];
      return config ? config.title : 'Unknown Chart';
    },

    getGraphIcon(graphType) {
      const config = this.graphConfig[graphType];
      return config ? config.icon : 'BarChart';
    },

    isValidGraphType(graphType) {
      return this.graphConfig.hasOwnProperty(graphType);
    }
  }
};
</script>

<style scoped>
/* Additional custom styles if needed */
.graph-container {
  min-height: 300px;
}

/* Smooth transitions for dashboard switching */
.dashboard-transition-enter-active,
.dashboard-transition-leave-active {
  transition: all 0.3s ease;
}

.dashboard-transition-enter-from,
.dashboard-transition-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>