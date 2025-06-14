<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Sidebar Component -->
    <Sidebar v-model="activeTab" @tab-changed="handleTabChange" />
    
    <!-- Main Content Area -->
    <div class="lg:ml-64 min-h-screen">
      <!-- Header -->
      <header class="bg-white/80 backdrop-blur-lg shadow-sm border-b border-gray-200/50 px-4 sm:px-6 lg:px-8 py-6 sticky top-0 z-20">
        <div class="flex items-center justify-between">
          <div class="ml-12 lg:ml-0">
            <h1 class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-500 to-purple-400 bg-clip-text text-transparent">
              {{ getPageTitle() }}
            </h1>
            <p class="text-gray-600 mt-1 text-sm sm:text-base">{{ getPageDescription() }}</p>
          </div>
          
          <!-- Status Indicator -->
          <div v-if="graphData.length > 0" class="hidden sm:flex items-center space-x-3 px-4 py-2 rounded-full bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200">
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-green-700">Data loaded successfully</span>
          </div>
        </div>
      </header>

      <!-- Content Area -->
      <main class="p-4 sm:p-6 lg:p-8">
        <!-- Dashboard Content -->
        <div v-if="activeTab === 'Dashboard'" class="space-y-6 sm:space-y-8">
          <!-- Stats Overview -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:transform hover:scale-105">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Total Files</p>
                  <p class="text-2xl font-bold text-gray-900">{{ graphData.length > 0 ? '1' : '0' }}</p>
                </div>
                <div class="w-12 h-12 rounded-xl flex items-center justify-center" style="background: linear-gradient(135deg, #7e52a0 0%, #d295bf 100%)">
                  <FileText class="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:transform hover:scale-105">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Active Charts</p>
                  <p class="text-2xl font-bold text-gray-900">3</p>
                </div>
                <div class="w-12 h-12 rounded-xl flex items-center justify-center" style="background: linear-gradient(135deg, #d295bf 0%, #e6bccd 100%)">
                  <BarChart3 class="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:transform hover:scale-105">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Data Points</p>
                  <p class="text-2xl font-bold text-gray-900">{{ graphData.length || '--' }}</p>
                </div>
                <div class="w-12 h-12 rounded-xl flex items-center justify-center" style="background: linear-gradient(135deg, #e6bccd 0%, #7e52a0 100%)">
                  <TrendingUp class="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:transform hover:scale-105">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Last Updated</p>
                  <p class="text-2xl font-bold text-gray-900">{{ getCurrentTime() }}</p>
                </div>
                <div class="w-12 h-12 rounded-xl flex items-center justify-center" style="background: linear-gradient(135deg, #7e52a0 0%, #e6bccd 100%)">
                  <Clock class="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          </div>

          <!-- File Upload Section -->
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 sm:p-8 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center space-x-4 mb-6">
              <div class="w-14 h-14 rounded-2xl flex items-center justify-center shadow-lg" style="background: linear-gradient(135deg, #7e52a0 0%, #d295bf 100%)">
                <Upload class="w-7 h-7 text-white" />
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Upload Data</h3>
                <p class="text-gray-600">Upload your data files to generate beautiful visualizations</p>
              </div>
            </div>
            <FileUpload @dataParsed="datainJSON" />
          </div>

          <!-- Graphs Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 sm:gap-8">
            <!-- Bar Graph -->
            <div class="group bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden hover:shadow-2xl transition-all duration-500 hover:transform hover:scale-[1.02]">
              <div class="p-6 border-b border-gray-100/50 flex items-center justify-between bg-gradient-to-r from-white/50 to-gray-50/50">
                <h4 class="font-bold text-gray-900 flex items-center text-lg">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3" style="background: linear-gradient(135deg, #7e52a0 0%, #d295bf 100%)">
                    <BarChart3 class="w-4 h-4 text-white" />
                  </div>
                  Bar Chart
                </h4>
                <DownloadChart :chartRef="bargraphref" filename="bar_graph.png" />
              </div>
              <div ref="bargraphref" class="p-6">
                <BarGraph 
                  title="Bar Graph" 
                  :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'" 
                />
              </div>
            </div>

            <!-- Doughnut Graph -->
            <div class="group bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden hover:shadow-2xl transition-all duration-500 hover:transform hover:scale-[1.02]">
              <div class="p-6 border-b border-gray-100/50 flex items-center justify-between bg-gradient-to-r from-white/50 to-gray-50/50">
                <h4 class="font-bold text-gray-900 flex items-center text-lg">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3" style="background: linear-gradient(135deg, #d295bf 0%, #e6bccd 100%)">
                    <PieChart class="w-4 h-4 text-white" />
                  </div>
                  Doughnut Chart
                </h4>
                <DownloadChart :chartRef="doughnutref" filename="doughnut_graph.png" />
              </div>
              <div ref="doughnutref" class="p-6">
                <Doughnut 
                  title="Doughnut" 
                  :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'" 
                />
              </div>
            </div>

            <!-- Pie Chart -->
            <div class="group bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden hover:shadow-2xl transition-all duration-500 hover:transform hover:scale-[1.02]">
              <div class="p-6 border-b border-gray-100/50 flex items-center justify-between bg-gradient-to-r from-white/50 to-gray-50/50">
                <h4 class="font-bold text-gray-900 flex items-center text-lg">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3" style="background: linear-gradient(135deg, #e6bccd 0%, #7e52a0 100%)">
                    <PieChart class="w-4 h-4 text-white" />
                  </div>
                  Pie Chart
                </h4>
                <DownloadChart :chartRef="piechartref" filename="piechart_graph.png" />
              </div>
              <div ref="piechartref" class="p-6">
                <PIEChart 
                  title="Pie Chart" 
                  :chartInput="graphData.length > 0 ? graphData : '/sampledata.json'" 
                />
              </div>
            </div>

            <!-- Placeholder Cards -->
            <div class="group bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden hover:shadow-2xl transition-all duration-500 hover:transform hover:scale-[1.02]">
              <div class="p-6 border-b border-gray-100/50 bg-gradient-to-r from-white/50 to-gray-50/50">
                <h4 class="font-bold text-gray-900 flex items-center text-lg">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3" style="background: linear-gradient(135deg, #7e52a0 0%, #d295bf 100%)">
                    <TrendingUp class="w-4 h-4 text-white" />
                  </div>
                  Line Chart
                </h4>
              </div>
              <div class="p-12 text-center text-gray-500">
                <div class="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center" style="background: linear-gradient(135deg, #e6bccd 0%, #d295bf 100%)">
                  <TrendingUp class="w-8 h-8 text-white" />
                </div>
                <p class="text-sm font-medium">Coming Soon</p>
                <p class="text-xs text-gray-400 mt-1">Advanced line visualizations</p>
              </div>
            </div>

            <div class="group bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden hover:shadow-2xl transition-all duration-500 hover:transform hover:scale-[1.02]">
              <div class="p-6 border-b border-gray-100/50 bg-gradient-to-r from-white/50 to-gray-50/50">
                <h4 class="font-bold text-gray-900 flex items-center text-lg">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3" style="background: linear-gradient(135deg, #d295bf 0%, #e6bccd 100%)">
                    <Activity class="w-4 h-4 text-white" />
                  </div>
                  Area Chart
                </h4>
              </div>
              <div class="p-12 text-center text-gray-500">
                <div class="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center" style="background: linear-gradient(135deg, #7e52a0 0%, #e6bccd 100%)">
                  <Activity class="w-8 h-8 text-white" />
                </div>
                <p class="text-sm font-medium">Coming Soon</p>
                <p class="text-xs text-gray-400 mt-1">Area and region charts</p>
              </div>
            </div>

            <div class="group bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden hover:shadow-2xl transition-all duration-500 hover:transform hover:scale-[1.02]">
              <div class="p-6 border-b border-gray-100/50 bg-gradient-to-r from-white/50 to-gray-50/50">
                <h4 class="font-bold text-gray-900 flex items-center text-lg">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3" style="background: linear-gradient(135deg, #e6bccd 0%, #7e52a0 100%)">
                    <BarChart class="w-4 h-4 text-white" />
                  </div>
                  Scatter Plot
                </h4>
              </div>
              <div class="p-12 text-center text-gray-500">
                <div class="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center" style="background: linear-gradient(135deg, #d295bf 0%, #7e52a0 100%)">
                  <BarChart class="w-8 h-8 text-white" />
                </div>
                <p class="text-sm font-medium">Coming Soon</p>
                <p class="text-xs text-gray-400 mt-1">Scatter and bubble charts</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Other Tab Contents -->
        <div v-else-if="activeTab === 'Your Files'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center">
            <myfiles />
          </div>
        </div>

        <div v-else-if="activeTab === 'Table'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center">
            <Yourtable />
          </div>
        </div>

        <div v-else-if="activeTab === 'Graphs'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center">
            <Yourgraph />
          </div>
        </div>

        <div v-else-if="activeTab === 'Account'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center">
            <div class="w-20 h-20 mx-auto mb-6 rounded-2xl flex items-center justify-center" style="background: linear-gradient(135deg, #d295bf 0%, #e6bccd 100%)">
              <User class="w-10 h-10 text-white" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Account Settings</h3>
            <p class="text-gray-600 mb-6">Manage your profile and preferences</p>
            <div class="inline-flex items-center px-6 py-3 rounded-xl text-white font-medium" style="background: linear-gradient(135deg, #e6bccd 0%, #7e52a0 100%)">
              <Clock class="w-4 h-4 mr-2" />
              Coming Soon
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import FileUpload from '@/components/FileUpload.vue';
import Doughnut from '@/components/DoughnutGraph.vue';
import BarGraph from '@/components/BarGraph.vue';
import PIEChart from '@/components/PieChart.vue';
import DownloadChart from '@/components/DownloadChart.vue';
import Yourtable from '@/views/Table.vue'
import Yourgraph from './Yourgraph.vue';
import Myfiles from './Myfiles.vue';
import { ref } from 'vue';
import { 
  Upload,
  PieChart as PieChartIcon,
  TrendingUp,
  Activity,
  BarChart,
  BarChart3,
  FileText,
  User,
  Clock
} from 'lucide-vue-next';

export default {
  name: 'Dashboard',
  components: {
    Sidebar,
    FileUpload,
    Doughnut,
    BarGraph,
    PIEChart,
    DownloadChart,
    Upload,
    PieChart: PieChartIcon,
    TrendingUp,
    Activity,
    BarChart,
    BarChart3,
    FileText,
    User,
    Clock,
    Yourtable,
    Yourgraph,
    Myfiles
  },
  setup() {
    const bargraphref = ref(null);
    const doughnutref = ref(null);
    const piechartref = ref(null);
    const graphData = ref([]);
    const activeTab = ref('Dashboard');

    const datainJSON = (data) => {
      graphData.value = data;
    };

    const handleTabChange = (tabName) => {
      activeTab.value = tabName;
    };

    const getPageTitle = () => {
      const titles = {
        'Dashboard': 'Data Visualization Dashboard',
        'Your Files': 'Your Files',
        'Graphs': 'Graph Library',
        'Table': 'Data Tables',
        'Account': 'Account Settings'
      };
      return titles[activeTab.value] || 'Dashboard';
    };

    const getPageDescription = () => {
      const descriptions = {
        'Dashboard': 'Create and manage your data visualizations with style',
        'Your Files': 'Manage your uploaded files and data sources',
        'Graphs': 'Explore different chart types and visualization options',
        'Table': 'Edit Your data table here',
        'Account': 'Manage your account settings and preferences'
      };
      return descriptions[activeTab.value] || '';
    };

    const getCurrentTime = () => {
      const now = new Date();
      return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
      });
    };
    
    return {
      datainJSON,
      graphData,
      bargraphref,
      doughnutref,
      piechartref,
      activeTab,
      handleTabChange,
      getPageTitle,
      getPageDescription,
      getCurrentTime
    };
  }
};
</script>