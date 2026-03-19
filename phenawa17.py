import React, { useState, useRef, useEffect } from 'react';
import { Upload, Camera, Loader2, X, Aperture } from 'lucide-react';

export default function PhenawaLuxPreview() {
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<{ type: string; tips: string[] } | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Cleanup camera on unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setIsCameraActive(true);
      setResult(null);
      setImagePreview(null);
    } catch (err) {
      console.error("Camera access denied:", err);
      alert("Please allow camera access to use this feature.");
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/jpeg');
        setImagePreview(dataUrl);
        stopCamera();
        runAnalysis();
      }
    }
  };

  const runAnalysis = () => {
    setAnalyzing(true);
    setResult(null);

    // Simulate AI processing time
    setTimeout(() => {
      setAnalyzing(false);
      // Simulate returning a "Rectangle / Slim" result
      setResult({
        type: "Rectangle / Slim",
        tips: [
          "Wear structured jackets.",
          "Horizontal stripes.",
          "Layer your clothing."
        ]
      });
    }, 2500);
  };

  const handleSimulateUpload = () => {
    // Simulate selecting an image
    setImagePreview("https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&q=80&w=800");
    runAnalysis();
  };

  const handleReset = () => {
    setImagePreview(null);
    setResult(null);
    stopCamera();
  };

  return (
    <div className="min-h-screen bg-[#FFFFF0] text-[#0A0A0A] font-sans selection:bg-black selection:text-white">
      <div className="max-w-2xl mx-auto px-6 py-12">
        
        {/* Header Section */}
        <div className="mb-10">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tighter uppercase border-b-2 border-black pb-3 mb-3">
            PHENAWA
          </h1>
          <h3 className="font-semibold uppercase text-xs md:text-sm tracking-[0.2em] text-[#555555]">
            The AI-Driven Personal Stylist
          </h3>
        </div>

        <p className="text-lg mb-8 leading-relaxed text-[#333333]">
          Upload a full-body photo to receive precise, geometry-based styling recommendations.
        </p>

        {/* Input Selection Area */}
        {!imagePreview && !analyzing && !isCameraActive && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div 
              onClick={handleSimulateUpload}
              className="border-2 border-[#CCCCCC] hover:border-black bg-white p-12 text-center cursor-pointer transition-colors duration-300 flex flex-col items-center justify-center group"
            >
              <Upload size={32} strokeWidth={1.5} className="mb-4 text-[#888888] group-hover:text-black transition-colors" />
              <p className="font-medium uppercase tracking-wider text-sm mb-1">Upload Photo</p>
              <p className="text-xs text-[#888888]">From Gallery</p>
            </div>

            <div 
              onClick={startCamera}
              className="border-2 border-[#0A0A0A] hover:bg-[#0A0A0A] hover:text-[#FFFFF0] bg-white text-[#0A0A0A] p-12 text-center cursor-pointer transition-colors duration-300 flex flex-col items-center justify-center group"
            >
              <Camera size={32} strokeWidth={1.5} className="mb-4 transition-colors" />
              <p className="font-medium uppercase tracking-wider text-sm mb-1">Open Camera</p>
              <p className="text-xs opacity-70">Live Scan</p>
            </div>
          </div>
        )}

        {/* Live Camera View */}
        {isCameraActive && (
          <div className="space-y-4 animate-in fade-in duration-500">
            <div className="relative border-4 border-[#0A0A0A] bg-black overflow-hidden h-[60vh] md:h-[500px] w-full flex items-center justify-center">
              <video 
                ref={videoRef} 
                autoPlay 
                playsInline 
                muted 
                className="w-full h-full object-cover"
              />
              
              {/* Camera UI Overlay */}
              <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/4 w-full h-px bg-white/30"></div>
                <div className="absolute top-3/4 w-full h-px bg-white/30"></div>
                <div className="absolute left-1/4 h-full w-px bg-white/30"></div>
                <div className="absolute left-3/4 h-full w-px bg-white/30"></div>
              </div>

              <button 
                onClick={stopCamera}
                className="absolute top-4 right-4 bg-white/10 hover:bg-white/30 text-white p-2 rounded-full backdrop-blur-sm transition-colors pointer-events-auto"
              >
                <X size={24} />
              </button>
            </div>
            
            <button 
              onClick={capturePhoto}
              className="w-full py-4 bg-[#0A0A0A] text-[#FFFFF0] uppercase tracking-wider text-sm font-bold hover:bg-[#333333] transition-colors duration-300 flex items-center justify-center gap-2"
            >
              <Aperture size={20} />
              Capture Frame
            </button>
            
            {/* Hidden canvas for taking the snapshot */}
            <canvas ref={canvasRef} className="hidden" />
          </div>
        )}

        {/* Loading State */}
        {analyzing && imagePreview && (
          <div className="space-y-6">
            <div className="relative h-64 md:h-96 w-full overflow-hidden bg-neutral-100 border border-[#E0E0E0]">
              <img src={imagePreview} alt="Preview" className="w-full h-full object-cover opacity-50 grayscale" />
              <div className="absolute inset-0 flex flex-col items-center justify-center text-black">
                <Loader2 size={40} className="animate-spin mb-4" />
                <p className="uppercase tracking-widest text-sm font-bold bg-[#FFFFF0]/80 px-4 py-2">Analyzing geometry...</p>
              </div>
            </div>
          </div>
        )}

        {/* Results State */}
        {result && !analyzing && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            
            <div className="h-64 md:h-96 w-full overflow-hidden border border-[#E0E0E0] relative">
              <img src={imagePreview!} alt="Analyzed" className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700" />
              <div className="absolute top-4 right-4 bg-black text-white text-xs font-bold px-3 py-1 uppercase tracking-wider">
                Scanned
              </div>
            </div>

            <div className="border border-[#E0E0E0] p-8 text-center bg-white shadow-sm">
              <h3 className="uppercase text-xs tracking-[0.2em] text-[#888888] mb-2 font-semibold">Detected Profile</h3>
              <h2 className="text-3xl font-bold uppercase tracking-tight">{result.type}</h2>
            </div>

            <div className="pt-4 border-t border-[#E0E0E0]">
              <h3 className="font-bold text-lg uppercase tracking-wider mb-6">Your Style Directives</h3>
              <ul className="space-y-4">
                {result.tips.map((tip, idx) => (
                  <li key={idx} className="flex items-start text-[#333333]">
                    <span className="mr-3 font-bold text-black">•</span>
                    <span className="text-lg">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>

            <button 
              onClick={handleReset}
              className="w-full py-4 bg-[#0A0A0A] text-[#FFFFF0] uppercase tracking-wider text-sm font-bold hover:bg-[#333333] transition-colors duration-300 mt-8"
            >
              Scan Another Profile
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
