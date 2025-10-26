import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import LiquidEther from '@/components/LiquidEther';
import TiltedCard from "@/components/TiltedCard";
import TextTrail from "@/components/TextTrail"; // Let's add the title too!

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    // --- 1. THE MAIN CONTAINER ---
    // We use `minHeight: '100vh'` to ensure it fills the entire screen height.
    // `display: 'flex'` and the other properties are for centering the content.
    <div style={{
      minHeight: '100vh',
      width: '100%',
      position: 'relative', // Establishes a positioning context for children
      display: 'flex',
      flexDirection: 'column', // Stack children vertically
      justifyContent: 'center',
      alignItems: 'center',
      overflow: 'hidden', // Prevents any weird overflow
      backgroundColor: '#000000', // A solid black background
      color: 'white',
    }}>

      {/* --- 2. THE BACKGROUND LAYER --- */}
      {/* This is layered behind everything else. It fills the entire container. */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 0 // Explicitly set as the bottom layer
      }}>
        <LiquidEther
    colors={[ '#5227FF', '#FF9FFC', '#B19EEF' ]}
    mouseForce={20}
    cursorSize={100}
    isViscous={false}
    viscous={30}
    iterationsViscous={32}
    iterationsPoisson={32}
    resolution={0.1}
    isBounce={false}
    autoDemo={true}
    autoSpeed={0.5}
    autoIntensity={2.2}
    takeoverDuration={0.25}
    autoResumeDelay={3000}
    autoRampDuration={0.6}
  />
      </div>

      {/* --- 3. THE CONTENT LAYER --- */}
      {/* This div sits on top of the background. `zIndex: 1` ensures it. */}
      {/* We use flexbox again to center the content inside it. */}
      <div style={{
        zIndex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '2rem', // Adds space between the title and the card
        textAlign: 'center'
      }}>
        <TextTrail
          text="404: Not Found"
          textColor="#ffffff"
          backgroundColor="transparent"
          noiseScale={0.002}
        />

        <p style={{ color: '#aaa', marginTop: '-2rem' }}>
          The page you're looking for doesn't exist.
        </p>

        {/* The TiltedCard is now a direct child of the content layer */}
        <TiltedCard
          imageSrc="https://i.scdn.co/image/ab67616d0000b273d9985092cd88bffd97653b58"
          altText="Kendrick Lamar - GNX Album Cover"
          captionText="Maybe listen to this instead?"
          containerHeight="300px"
          containerWidth="300px"
          imageHeight="300px"
          imageWidth="300px"
          rotateAmplitude={12}
          scaleOnHover={1.15}
          showMobileWarning={false}
          showTooltip={true}
        />
      </div>
    </div>
  );
};

export default NotFound;
