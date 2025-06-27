import apiClient from './apiClient' // Adjust the import based on your project structure

export const graphdbApi = {
  async processForGraphDB(setId, requestData) {
    const response = await apiClient.post(`/datasources/${setId}/graphdb-process`, requestData)
    return response.data
  }
}