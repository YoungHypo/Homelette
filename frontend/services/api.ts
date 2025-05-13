import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// 设置基础URL - 根据您的Flask API部署情况调整
const BASE_URL = 'http://localhost:5001/api';

// 创建axios实例
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 从AsyncStorage中获取token的辅助函数
const getAuthToken = async () => {
  try {
    return await AsyncStorage.getItem('authToken');
  } catch (error) {
    console.error('Error getting token from AsyncStorage:', error);
    return null;
  }
};

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  async (config) => {
    const token = await getAuthToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api; 