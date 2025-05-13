import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface SignUpOptions {
  major?: string;
  graduationYear?: number;
  aboutMe?: string;
  profilePicture?: {
    uri: string;
    name: string;
    type: string;
  };
  phone?: string;
}

// 用户登录
export const signIn = async (email: string, password: string) => {
  try {
    const response = await api.post('/auth/login', {
      email,
      password
    });
    
    const { token, user } = response.data;
    
    // 存储认证令牌和用户信息
    await AsyncStorage.setItem('authToken', token);
    await AsyncStorage.setItem('user', JSON.stringify(user));
    
    return user;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

// 用户注册
export const signUp = async (
  email: string, 
  password: string, 
  firstName: string, 
  lastName: string, 
  options: SignUpOptions = {}
) => {
  try {
    // 创建表单数据对象，用于处理文件上传
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('firstName', firstName);
    formData.append('lastName', lastName);
    
    // 添加可选字段
    if (options.major) formData.append('major', options.major);
    if (options.graduationYear) formData.append('graduationYear', options.graduationYear.toString());
    if (options.aboutMe) formData.append('aboutMe', options.aboutMe);
    if (options.phone) formData.append('phone', options.phone);
    
    // 处理头像上传
    if (options.profilePicture) {
      formData.append('profilePicture', {
        uri: options.profilePicture.uri,
        name: options.profilePicture.name,
        type: options.profilePicture.type,
      } as any);
    }
    
    const response = await api.post('/auth/register', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    const { token, user } = response.data;
    
    // 存储认证令牌和用户信息
    await AsyncStorage.setItem('authToken', token);
    await AsyncStorage.setItem('user', JSON.stringify(user));
    
    return user;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

// 用户登出
export const signOut = async () => {
  try {
    await AsyncStorage.removeItem('authToken');
    await AsyncStorage.removeItem('user');
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
};

// 获取当前用户信息
export const getCurrentUser = async () => {
  try {
    const userJson = await AsyncStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
  } catch (error) {
    console.error('Get current user error:', error);
    return null;
  }
}; 