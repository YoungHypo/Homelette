import React from 'react';
import { Text, TextProps } from 'react-native';

interface ThemedTextProps extends TextProps {
  children: React.ReactNode;
}

export function ThemedText(props: ThemedTextProps) {
  const { style, ...otherProps } = props;
  return (
    <Text 
      style={[
        { color: '#000000' }, // 默认颜色
        style
      ]} 
      {...otherProps}
    />
  );
} 