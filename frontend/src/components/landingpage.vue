<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <div class="w-64 bg-white shadow-lg border-r border-gray-200">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-800">Dashboard</h2>
      </div>
      
      <nav class="mt-6">
        <div class="px-3 space-y-1">
          <button
            v-for="item in sidebarItems"
            :key="item.name"
            @click="activeTab = item.name"
            :class="[
              'w-full flex items-center px-3 py-3 text-left rounded-lg transition-all duration-200 group',
              activeTab === item.name
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            ]"
          >
            <component 
              :is="item.icon" 
              :class="[
                'w-5 h-5 mr-3 transition-colors duration-200',
                activeTab === item.name ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'
              ]"
            />
            <span class="font-medium">{{ item.name }}</span>
          </button>
        </div>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-auto">
      <!-- Header -->
      <header class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ getPageTitle() }}</h1>
            <p class="text-gray-600 mt-1">{{ getPageDescription() }}</p>
          </div>
          
          <!-- Status Indicator -->
          <div v-if="graphData.length > 0" class="flex items-center space-x-2">
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-green-700">Data loaded successfully</span>
          </div>
        </div>
      </header>

      <!-- Content Area -->
      <main class="p-6">
        <!-- Dashboard Content -->
        <div v-if="activeTab === 'Dashboard'" class="space-y-6">
          <!-- File Upload Section -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Upload class="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">Upload Data</h3>
                <p class="text-sm text-gray-600">Upload your data files to generate visualizations</p>
              </div>
            </div>
            <FileUpload @dataParsed="datainJSON" />
          </div>

          <!-- Graphs Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            <!-- Bar Graph -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200">
              <div class="p-4 border-b border-gray-100 flex items-center justify-between">
                <h4 class="font-semibold text-gray-900 flex items-center">
                  <BarChart3 class="w-4 h-4 mr-2 text-blue-600" />
                  Bar Chart
                </h4>
                <DownloadChart :chartRef="bargraphref" filename="bar_graph.png" />
              </div>
              <div ref="bargraphref" class="p-4">
                <BarGraph 
                  title="Bar Graph" 
                  :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'" 
                />
              </div>
            </div>

            <!-- Doughnut Graph -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200">
              <div class="p-4 border-b border-gray-100 flex items-center justify-between">
                <h4 class="font-semibold text-gray-900 flex items-center">
                  <PieChart class="w-4 h-4 mr-2 text-green-600" />
                  Doughnut Chart
                </h4>
                <DownloadChart :chartRef="doughnutref" filename="doughnut_graph.png" />
              </div>
              <div ref="doughnutref" class="p-4">
                <Doughnut 
                  title="Doughnut" 
                  :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'" 
                />
              </div>
            </div>

            <!-- Pie Chart -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200">
              <div class="p-4 border-b border-gray-100 flex items-center justify-between">
                <h4 class="font-semibold text-gray-900 flex items-center">
                  <PieChart class="w-4 h-4 mr-2 text-purple-600" />
                  Pie Chart
                </h4>
                <DownloadChart :chartRef="piechartref" filename="piechart_graph.png" />
              </div>
              <div ref="piechartref" class="p-4">
                <PIEChart 
                  title="Pie Chart" 
                  :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'" 
                />
              </div>
            </div>

            <!-- Placeholder Cards -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200">
              <div class="p-4 border-b border-gray-100">
                <h4 class="font-semibold text-gray-900 flex items-center">
                  <TrendingUp class="w-4 h-4 mr-2 text-orange-600" />
                  Line Chart
                </h4>
              </div>
              <div class="p-8 text-center text-gray-500">
                <TrendingUp class="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p class="text-sm">Coming Soon</p>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200">
              <div class="p-4 border-b border-gray-100">
                <h4 class="font-semibold text-gray-900 flex items-center">
                  <Activity class="w-4 h-4 mr-2 text-red-600" />
                  Area Chart
                </h4>
              </div>
              <div class="p-8 text-center text-gray-500">
                <Activity class="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p class="text-sm">Coming Soon</p>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200">
              <div class="p-4 border-b border-gray-100">
                <h4 class="font-semibold text-gray-900 flex items-center">
                  <BarChart class="w-4 h-4 mr-2 text-indigo-600" />
                  Scatter Plot
                </h4>
              </div>
              <div class="p-8 text-center text-gray-500">
                <BarChart class="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p class="text-sm">Coming Soon</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Other Tab Contents -->
        <div v-else-if="activeTab === 'Your Files'" class="space-y-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <FileText class="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Your Files</h3>
            <p class="text-gray-600">File management section coming soon</p>
          </div>
        </div>

        <div v-else-if="activeTab === 'Graphs'" class="space-y-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <BarChart3 class="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Graph Library</h3>
            <p class="text-gray-600">Advanced graph options coming soon</p>
          </div>
        </div>

        <div v-else-if="activeTab === 'Account'" class="space-y-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <User class="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Account Settings</h3>
            <p class="text-gray-600">Account management coming soon</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import FileUpload from './FileUpload.vue';
import Doughnut from './DoughnutGraph.vue';
import BarGraph from './BarGraph.vue';
import PIEChart from './PieChart.vue';
import DownloadChart from './DownloadChart.vue';
import { ref } from 'vue';
import { 
  LayoutDashboard, 
  FileText, 
  BarChart3, 
  User,
  Upload,
  PieChart as PieChartIcon,
  TrendingUp,
  Activity,
  BarChart
} from 'lucide-vue-next';

export default {
  name: 'LandingPage',
  components: {
    FileUpload,
    Doughnut,
    BarGraph,
    PIEChart,
    DownloadChart,
    LayoutDashboard,
    FileText,
    BarChart3,
    User,
    Upload,
    PieChart: PieChartIcon,
    TrendingUp,
    Activity,
    BarChart
  },
  setup() {
    const bargraphref = ref(null);
    const doughnutref = ref(null);
    const piechartref = ref(null);
    const graphData = ref([]);
    const activeTab = ref('Dashboard');

    const sidebarItems = ref([
      { name: 'Dashboard', icon: 'LayoutDashboard' },
      { name: 'Your Files', icon: 'FileText' },
      { name: 'Graphs', icon: 'BarChart3' },
      { name: 'Account', icon: 'User' }
    ]);

    const datainJSON = (data) => {
      graphData.value = data;
    };

    const getPageTitle = () => {
      const titles = {
        'Dashboard': 'Data Visualization Dashboard',
        'Your Files': 'Your Files',
        'Graphs': 'Graph Library',
        'Account': 'Account Settings'
      };
      return titles[activeTab.value] || 'Dashboard';
    };

    const getPageDescription = () => {
      const descriptions = {
        'Dashboard': 'Create and manage your data visualizations',
        'Your Files': 'Manage your uploaded files',
        'Graphs': 'Explore different chart types and options',
        'Account': 'Manage your account settings and preferences'
      };
      return descriptions[activeTab.value] || '';
    };
    
    return {
      datainJSON,
      graphData,
      bargraphref,
      doughnutref,
      piechartref,
      activeTab,
      sidebarItems,
      getPageTitle,
      getPageDescription
    };
  }
};
</script>