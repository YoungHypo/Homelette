import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import Svg, { Path, Defs, LinearGradient, Stop } from 'react-native-svg';

const { width, height } = Dimensions.get('window');

export function WaveBackground() {
  return (
    <View style={StyleSheet.absoluteFill}>
      <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
        <Defs>
          <LinearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor="#B3E0FF" stopOpacity="1" />
            <Stop offset="0.5" stopColor="#4DA6FF" stopOpacity="1" />
            <Stop offset="1" stopColor="#0066CC" stopOpacity="1" />
          </LinearGradient>
        </Defs>
        <Path
          d={`
            M0 0
            L0 ${height}
            L${width} ${height}
            L${width} 0
            Z
          `}
          fill="url(#grad)"
        />
        <Path
          d={`
            M0 ${height * 0.45}
            Q ${width * 0.2} ${height * 0.43} ${width * 0.4} ${height * 0.45}
            T ${width * 0.8} ${height * 0.45}
            T ${width} ${height * 0.45}
            L${width} ${height}
            L0 ${height}
            Z
          `}
          fill="#66B2FF"
          opacity="0.4"
        />
        <Path
          d={`
            M0 ${height * 0.55}
            Q ${width * 0.25} ${height * 0.53} ${width * 0.5} ${height * 0.55}
            T ${width} ${height * 0.55}
            L${width} ${height}
            L0 ${height}
            Z
          `}
          fill="#3399FF"
          opacity="0.5"
        />
        <Path
          d={`
            M0 ${height * 0.65}
            Q ${width * 0.15} ${height * 0.63} ${width * 0.3} ${height * 0.65}
            T ${width * 0.6} ${height * 0.65}
            T ${width} ${height * 0.65}
            L${width} ${height}
            L0 ${height}
            Z
          `}
          fill="#0080FF"
          opacity="0.6"
        />
        <Path
          d={`
            M0 ${height}
            L0 ${height * 0.80}
            Q ${width * 0.25} ${height * 0.78} ${width * 0.5} ${height * 0.80}
            T ${width} ${height * 0.80}
            L${width} ${height}
            Z
          `}
          fill="#0066CC"
          opacity="0.7"
        />
        <Path
          d={`
            M0 ${height * 0.35}
            Q ${width * 0.3} ${height * 0.32} ${width * 0.6} ${height * 0.35}
            T ${width} ${height * 0.35}
            L${width} ${height}
            L0 ${height}
            Z
          `}
          fill="#99CCFF"
          opacity="0.3"
        />
      </Svg>
    </View>
  );
} 