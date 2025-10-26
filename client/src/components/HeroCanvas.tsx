import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Icosahedron } from '@react-three/drei';
import * as THREE from 'three';

const Shape = ({ position, color, speed }: { position: [number, number, number], color: string, speed: number }) => {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * speed;
      meshRef.current.rotation.y += delta * speed;
    }
  });

  return (
    <Icosahedron ref={meshRef} args={[0.8, 0]} position={position}>
      <meshStandardMaterial color={color} roughness={0.5} metalness={0.1} />
    </Icosahedron>
  );
};

const HeroCanvas = () => {
  return (
    <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
      <ambientLight intensity={1.5} />
      <pointLight position={[10, 10, 10]} intensity={100} />
      <pointLight position={[-10, -10, 5]} intensity={50} />

      <Shape position={[-4, 2, 0]} color="#00a99d" speed={0.1} />
      <Shape position={[4, -2, -2]} color="#4285f4" speed={0.05} />
      <Shape position={[0, -3, 2]} color="#888888" speed={0.08} />
      <Shape position={[5, 4, -1]} color="#00a99d" speed={0.03} />
    </Canvas>
  );
};

export default HeroCanvas;