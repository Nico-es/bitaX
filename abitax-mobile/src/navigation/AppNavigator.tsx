import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import { useAuth } from '../contexts/AuthContext';

import { LoginScreen } from '../screens/LoginScreen';
import { RegisterScreen } from '../screens/RegisterScreen';
import { HomeScreen } from '../screens/HomeScreen';
import { PropertiesScreen } from '../screens/PropertiesScreen';
import { ServicesScreen } from '../screens/ServicesScreen';
import { ProfessionalsScreen } from '../screens/ProfessionalsScreen';
import { ProfileScreen } from '../screens/ProfileScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const AuthStack = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Login" component={LoginScreen} />
    <Stack.Screen name="Register" component={RegisterScreen} />
  </Stack.Navigator>
);

const MainTabs = () => (
  <Tab.Navigator
    screenOptions={{
      tabBarActiveTintColor: '#3b82f6',
      tabBarInactiveTintColor: '#666',
      tabBarStyle: {
        borderTopWidth: 1,
        borderTopColor: '#e0e0e0',
        paddingBottom: 8,
        paddingTop: 8,
        height: 60,
      },
      headerStyle: {
        backgroundColor: '#fff',
        elevation: 0,
        shadowOpacity: 0,
        borderBottomWidth: 1,
        borderBottomColor: '#e0e0e0',
      },
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}
  >
    <Tab.Screen
      name="Home"
      component={HomeScreen}
      options={{
        tabBarLabel: 'Home',
        tabBarIcon: ({ color }) => <span style={{ fontSize: 24 }}>🏠</span>,
      }}
    />
    <Tab.Screen
      name="Properties"
      component={PropertiesScreen}
      options={{
        tabBarLabel: 'Properties',
        tabBarIcon: ({ color }) => <span style={{ fontSize: 24 }}>🏢</span>,
      }}
    />
    <Tab.Screen
      name="Services"
      component={ServicesScreen}
      options={{
        tabBarLabel: 'Services',
        tabBarIcon: ({ color }) => <span style={{ fontSize: 24 }}>🔧</span>,
      }}
    />
    <Tab.Screen
      name="Professionals"
      component={ProfessionalsScreen}
      options={{
        tabBarLabel: 'Professionals',
        tabBarIcon: ({ color }) => <span style={{ fontSize: 24 }}>👔</span>,
      }}
    />
    <Tab.Screen
      name="Profile"
      component={ProfileScreen}
      options={{
        tabBarLabel: 'Profile',
        tabBarIcon: ({ color }) => <span style={{ fontSize: 24 }}>👤</span>,
      }}
    />
  </Tab.Navigator>
);

export const AppNavigator = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return null;
  }

  return (
    <NavigationContainer>
      {user ? <MainTabs /> : <AuthStack />}
    </NavigationContainer>
  );
};
