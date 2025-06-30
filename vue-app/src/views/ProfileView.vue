<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <!-- Alert Component -->
    <div v-if="alert.show" :class="`rounded-md ${alert.type === 'success' ? 'bg-green-50' : 'bg-red-50'} p-4 mb-4`">
      <div class="flex">
        <div class="flex-shrink-0">
          <CheckCircleIcon v-if="alert.type === 'success'" class="h-5 w-5 text-green-400" />
          <XCircleIcon v-else class="h-5 w-5 text-red-400" />
        </div>
        <div class="ml-3">
          <p :class="`text-sm font-medium ${alert.type === 'success' ? 'text-green-800' : 'text-red-800'}`">
            {{ alert.message }}
          </p>
        </div>
        <div class="ml-auto pl-3">
          <div class="-mx-1.5 -my-1.5">
            <button
              type="button"
              @click="clearAlert"
              :class="`inline-flex rounded-md ${alert.type === 'success' ? 'bg-green-50 text-green-500 hover:bg-green-100' : 'bg-red-50 text-red-500 hover:bg-red-100'} p-1.5`"
            >
              <span class="sr-only">Dismiss</span>
              <XMarkIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="animate-pulse">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
          <div class="h-6 bg-slate-200 rounded w-1/4 mb-4"></div>
          <div class="h-4 bg-slate-200 rounded w-1/2"></div>
        </div>
        <div class="border-t border-gray-200">
          <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <div class="h-4 bg-slate-200 rounded w-1/4"></div>
            <div class="h-4 bg-slate-200 rounded w-3/4 mt-2 sm:mt-0"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile content -->
    <div v-else class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">Profile Information</h3>
        <p class="mt-1 text-sm text-gray-500">
          Your account details and preferences.
        </p>
      </div>

      <div class="border-t border-gray-200">
        <dl>
          <!-- Name Section -->
          <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm font-medium text-gray-500">Full name</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <div v-if="!isEditingName" class="flex items-center justify-between">
                <span>{{ user.name || 'Not set' }}</span>
                <button
                  @click="startEditingName"
                  class="text-indigo-600 hover:text-indigo-900 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded-md px-2 py-1"
                >
                  Edit
                </button>
              </div>
              <div v-else class="flex items-center gap-2">
                <input
                  type="text"
                  v-model="nameEdit"
                  @keyup.enter="saveName"
                  class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Enter your name"
                  :disabled="isSaving"
                />
                <button
                  @click="saveName"
                  :disabled="isSaving || !nameEdit.trim()"
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ isSaving ? 'Saving...' : 'Save' }}
                </button>
                <button
                  @click="cancelEditName"
                  :disabled="isSaving"
                  class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  Cancel
                </button>
              </div>
            </dd>
          </div>

          <!-- Email Section -->
          <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm font-medium text-gray-500">Email address</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {{ user.email }}
            </dd>
          </div>

          <!-- API Key Section -->
          <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm font-medium text-gray-500">API Key</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <div class="flex items-center gap-2">
                <div class="relative flex-grow">
                  <input
                    :type="showApiKey ? 'text' : 'password'"
                    v-model="user.api_key"
                    readonly
                    class="shadow-sm block w-full sm:text-sm border-gray-300 rounded-md bg-gray-50"
                  />
                </div>
                <button
                  @click="toggleApiKeyVisibility"
                  class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <EyeIcon v-if="!showApiKey" class="h-4 w-4 mr-1" />
                  <EyeSlashIcon v-else class="h-4 w-4 mr-1" />
                  {{ showApiKey ? 'Hide' : 'Show' }}
                </button>
                <button
                  @click="copyApiKey"
                  class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <ClipboardIcon class="h-4 w-4 mr-1" />
                  Copy
                </button>
                <button
                  @click="regenerateApiKey"
                  :disabled="isRegeneratingKey"
                  class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  <ArrowPathIcon :class="{'animate-spin': isRegeneratingKey}" class="h-4 w-4 mr-1" />
                  {{ isRegeneratingKey ? 'Regenerating...' : 'Regenerate' }}
                </button>
              </div>
            </dd>
          </div>

          <!-- Password Section -->
          <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm font-medium text-gray-500">Password</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <button
                @click="openChangePassword"
                class="text-indigo-600 hover:text-indigo-900 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded-md px-2 py-1"
              >
                Change password
              </button>
            </dd>
          </div>

          <!-- Notification Preferences -->
          <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm font-medium text-gray-500">Notification preferences</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 space-y-4">
              <div class="relative flex items-start">
                <div class="flex items-center h-5">
                  <input
                    id="email-notifications"
                    v-model="notificationPreferences.emailNotifications"
                    type="checkbox"
                    :disabled="isSavingPreferences"
                    @change="saveNotificationPreferences"
                    class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div class="ml-3 text-sm">
                  <label for="email-notifications" class="font-medium text-gray-700">Email notifications</label>
                  <p class="text-gray-500">Receive email updates about your account and activities.</p>
                </div>
              </div>
              
              <div class="relative flex items-start">
                <div class="flex items-center h-5">
                  <input
                    id="analysis-updates"
                    v-model="notificationPreferences.analysisUpdates"
                    type="checkbox"
                    :disabled="isSavingPreferences"
                    @change="saveNotificationPreferences"
                    class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div class="ml-3 text-sm">
                  <label for="analysis-updates" class="font-medium text-gray-700">Analysis updates</label>
                  <p class="text-gray-500">Get notified when your data analysis tasks are completed.</p>
                </div>
              </div>
            </dd>
          </div>
        </dl>
      </div>
    </div>

    <!-- Change Password Modal -->
    <TransitionRoot appear :show="isChangePasswordOpen" as="template">
      <Dialog as="div" class="relative z-10" @close="closeChangePassword">
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="ease-out duration-300"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="ease-in duration-200"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                  Change Password
                </DialogTitle>

                <form @submit.prevent="handlePasswordChange" class="mt-4 space-y-4">
                  <div>
                    <label for="current-password" class="block text-sm font-medium text-gray-700">Current password</label>
                    <input
                      type="password"
                      id="current-password"
                      v-model="passwordForm.currentPassword"
                      required
                      :disabled="isChangingPassword"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="new-password" class="block text-sm font-medium text-gray-700">New password</label>
                    <input
                      type="password"
                      id="new-password"
                      v-model="passwordForm.newPassword"
                      required
                      :disabled="isChangingPassword"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="confirm-password" class="block text-sm font-medium text-gray-700">Confirm new password</label>
                    <input
                      type="password"
                      id="confirm-password"
                      v-model="passwordForm.confirmPassword"
                      required
                      :disabled="isChangingPassword"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                    <p v-if="passwordMismatchError" class="mt-1 text-sm text-red-600">
                      {{ passwordMismatchError }}
                    </p>
                  </div>
                  <div class="mt-6 flex justify-end space-x-2">
                    <button
                      type="button"
                      :disabled="isChangingPassword"
                      @click="closeChangePassword"
                      class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      :disabled="isChangingPassword || !isPasswordFormValid"
                      class="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
                    >
                      {{ isChangingPassword ? 'Updating...' : 'Update password' }}
                    </button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
import { 
  EyeIcon, 
  EyeSlashIcon, 
  ArrowPathIcon, 
  XCircleIcon, 
  CheckCircleIcon,
  ClipboardIcon,
  XMarkIcon 
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

// User data and loading states
const isLoading = ref(true)
const isSaving = ref(false)
const isRegeneratingKey = ref(false)
const isSavingPreferences = ref(false)
const user = computed(() => auth.user || {})

// Alert system
const alert = reactive({
  show: false,
  type: 'success',
  message: ''
})

function showAlert(message, type = 'success', duration = 3000) {
  alert.message = message
  alert.type = type
  alert.show = true
  if (duration) {
    setTimeout(() => {
      clearAlert()
    }, duration)
  }
}

function clearAlert() {
  alert.show = false
  alert.message = ''
}

// Name editing
const isEditingName = ref(false)
const nameEdit = ref('')

function startEditingName() {
  nameEdit.value = user.value.name || ''
  isEditingName.value = true
}

function cancelEditName() {
  isEditingName.value = false
  nameEdit.value = ''
}

async function saveName() {
  if (!nameEdit.value.trim()) return

  isSaving.value = true
  try {
    await auth.updateProfile({ name: nameEdit.value.trim() })
    isEditingName.value = false
    showAlert('Name updated successfully')
  } catch (error) {
    showAlert(error.message || 'Failed to update name', 'error')
  } finally {
    isSaving.value = false
  }
}

// API Key management
const showApiKey = ref(false)

function toggleApiKeyVisibility() {
  showApiKey.value = !showApiKey.value
}

async function copyApiKey() {
  try {
    await navigator.clipboard.writeText(user.value.api_key)
    showAlert('API key copied to clipboard')
  } catch (error) {
    showAlert('Failed to copy API key', 'error')
  }
}

async function regenerateApiKey() {
  const confirmed = await confirm('Are you sure you want to regenerate your API key? This will invalidate the existing key.')
  if (!confirmed) return

  isRegeneratingKey.value = true
  try {
    await auth.regenerateApiKey()
    showAlert('API key regenerated successfully')
  } catch (error) {
    showAlert(error.message || 'Failed to regenerate API key', 'error')
  } finally {
    isRegeneratingKey.value = false
  }
}

// Password management
const isChangePasswordOpen = ref(false)
const isChangingPassword = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordMismatchError = computed(() => {
  if (!passwordForm.confirmPassword) return ''
  return passwordForm.newPassword !== passwordForm.confirmPassword 
    ? 'Passwords do not match' 
    : ''
})

const isPasswordFormValid = computed(() => {
  return passwordForm.currentPassword &&
    passwordForm.newPassword &&
    passwordForm.confirmPassword &&
    passwordForm.newPassword === passwordForm.confirmPassword &&
    passwordForm.newPassword.length >= 8
})

function openChangePassword() {
  isChangePasswordOpen.value = true
}

function closeChangePassword() {
  isChangePasswordOpen.value = false
  passwordForm.currentPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}

async function handlePasswordChange() {
  if (!isPasswordFormValid.value) return
  
  isChangingPassword.value = true
  try {
    await auth.updatePassword({
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })
    showAlert('Password updated successfully')
    closeChangePassword()
  } catch (error) {
    showAlert(error.message || 'Failed to update password', 'error')
  } finally {
    isChangingPassword.value = false
  }
}

// Notification preferences
const notificationPreferences = reactive({
  emailNotifications: computed(() => user.value?.preferences?.emailNotifications ?? true),
  analysisUpdates: computed(() => user.value?.preferences?.analysisUpdates ?? true)
})

async function saveNotificationPreferences() {
  isSavingPreferences.value = true
  try {
    await auth.updateProfile({
      preferences: {
        emailNotifications: notificationPreferences.emailNotifications,
        analysisUpdates: notificationPreferences.analysisUpdates
      }
    })
    showAlert('Notification preferences updated')
  } catch (error) {
    showAlert(error.message || 'Failed to update notification preferences', 'error')
  } finally {
    isSavingPreferences.value = false
  }
}

// Initial load
onMounted(async () => {
  try {
    await auth.fetchUserProfile()
  } catch (error) {
    showAlert(error.message || 'Failed to load profile', 'error')
  } finally {
    isLoading.value = false
  }
})
</script>