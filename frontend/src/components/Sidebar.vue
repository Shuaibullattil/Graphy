<template>
  <!-- Mobile Overlay -->
  <div 
    v-if="isMobileMenuOpen" 
    class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
    @click="closeMobileMenu"
  ></div>

  <!-- Sidebar -->
  <div 
    :class="[
      'fixed left-0 top-0 h-full bg-white shadow-2xl border-r border-gray-100 z-50 transform transition-transform duration-300 ease-in-out',
      'w-64 lg:translate-x-0',
      isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
    ]"
  >
    <!-- Header -->
    <div class="flex items-center justify-between p-6 border-b border-gray-100">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background-color: #7e52a0;">
          <BarChart3 class="w-5 h-5 text-white" />
        </div>
        <h2 class="text-xl font-bold text-gray-800">Graphy</h2>
      </div>
      
      <!-- Mobile Close Button -->
      <button
        @click="closeMobileMenu"
        class="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
      >
        <X class="w-5 h-5 text-gray-600" />
      </button>
    </div>
    
    <!-- Navigation -->
    <nav class="mt-6 px-4 pb-6 overflow-y-auto">
      <div class="space-y-2">
        <button
          v-for="item in sidebarItems"
          :key="item.name"
          @click="selectItem(item.name)"
          :class="[
            'w-full flex items-center px-4 py-3 text-left rounded-xl transition-all duration-200 group relative overflow-hidden',
            activeTab === item.name
              ? 'text-white shadow-lg transform scale-[1.02]'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 hover:transform hover:scale-[1.01]'
          ]"
          :style="activeTab === item.name ? `background: linear-gradient(135deg, #7e52a0 0%, #d295bf 100%)` : ''"
        >
          <!-- Active background gradient -->
          <div 
            v-if="activeTab === item.name"
            class="absolute inset-0 opacity-10"
            style="background: linear-gradient(135deg, #e6bccd 0%, #d295bf 100%)"
          ></div>
          
          <component 
            :is="item.icon" 
            :class="[
              'w-5 h-5 mr-3 transition-all duration-200 relative z-10',
              activeTab === item.name 
                ? 'text-white' 
                : 'text-gray-400 group-hover:text-gray-600'
            ]"
          />
          <span 
            :class="[
              'font-medium relative z-10 transition-all duration-200',
              activeTab === item.name ? 'text-white' : ''
            ]"
          >
            {{ item.name }}
          </span>
          
          <!-- Active indicator -->
          <div 
            v-if="activeTab === item.name"
            class="absolute right-2 w-2 h-2 rounded-full bg-white opacity-80"
          ></div>
        </button>
      </div>

      <!-- User Profile Section -->
      <div class="mt-8 pt-6 border-t border-gray-100">
        <div class="flex items-center px-4 py-3 rounded-xl bg-gradient-to-r from-gray-50 to-gray-100">
          <div 
            class="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-semibold"
            style="background: linear-gradient(135deg, #7e52a0 0%, #d295bf 100%)"
          >
            JD
          </div>
          <div class="ml-3 min-w-0 flex-1">
            <p class="text-sm font-medium text-gray-900 truncate">John Doe</p>
            <p class="text-xs text-gray-500 truncate">john@example.com</p>
          </div>
        </div>
      </div>
    </nav>
  </div>

  <!-- Mobile Menu Button -->
  <button
    @click="openMobileMenu"
    class="fixed top-4 left-4 z-30 lg:hidden p-3 rounded-xl bg-white shadow-lg border border-gray-200 hover:shadow-xl transition-all duration-200"
    style="background: linear-gradient(135deg, #7e52a0 0%, #d295bf 100%)"
  >
    <Menu class="w-5 h-5 text-white" />
  </button>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { 
  LayoutDashboard, 
  FileText, 
  BarChart3, 
  User,
  Menu,
  X
} from 'lucide-vue-next';

export default {
  name: 'Sidebar',
  components: {
    LayoutDashboard,
    FileText,
    BarChart3,
    User,
    Menu,
    X
  },
  props: {
    modelValue: {
      type: String,
      default: 'Dashboard'
    }
  },
  emits: ['update:modelValue', 'tab-changed'],
  setup(props, { emit }) {
    const activeTab = ref(props.modelValue);
    const isMobileMenuOpen = ref(false);

    const sidebarItems = ref([
      { name: 'Dashboard', icon: 'LayoutDashboard' },
      { name: 'Your Files', icon: 'FileText' },
      { name: 'Graphs', icon: 'BarChart3' },
      { name: 'Account', icon: 'User' }
    ]);

    const selectItem = (itemName) => {
      activeTab.value = itemName;
      emit('update:modelValue', itemName);
      emit('tab-changed', itemName);
      closeMobileMenu();
    };

    const openMobileMenu = () => {
      isMobileMenuOpen.value = true;
    };

    const closeMobileMenu = () => {
      isMobileMenuOpen.value = false;
    };

    // Handle window resize
    const handleResize = () => {
      if (window.innerWidth >= 1024) {
        isMobileMenuOpen.value = false;
      }
    };

    onMounted(() => {
      window.addEventListener('resize', handleResize);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize);
    });

    return {
      activeTab,
      sidebarItems,
      isMobileMenuOpen,
      selectItem,
      openMobileMenu,
      closeMobileMenu
    };
  }
};
</script>