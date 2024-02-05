import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Button,
  TextField,
  Typography,
  Grid,
  Paper,
  ThemeProvider,
  createTheme,
} from '@mui/material';

const WasteStationPage = () => {
  const [stations, setStations] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentStationId, setCurrentStationId] = useState(null);
  const [showAutoCollectButton, setShowAutoCollectButton] = useState(true);

  const fetchStations = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/waste_stations/');
      setStations(response.data);

      // Verificar se o botão "Coleta Automaticamente" deve ser exibido
      const shouldShowButton = response.data.some(station => station.volume_percentage >= 80);
      setShowAutoCollectButton(shouldShowButton);
    } catch (error) {
      console.error('Erro ao buscar as estações:', error);
    }
  };

  const handleCollectRequest = async (id) => {
    try {
      const currentStation = stations.find((station) => station.id === id);

      if (currentStation && currentStation.volume_percentage >= 80) {
        setCurrentStationId(id);
        setShowModal(true);
      } else {
        await axios.patch(`http://127.0.0.1:8000/api/waste_stations/${id}/`, {
          collection_requested: true,
        });
        fetchStations();
      }
    } catch (error) {
      console.error('Erro ao solicitar a coleta:', error);
    }
  };

  const handleCollectConfirmation = async () => {
    try {
      if (currentStationId !== null) {
        await axios.patch(`http://127.0.0.1:8000/api/waste_stations/${currentStationId}/`, {
          collection_requested: false,
          collection_confirmed: true,
          volume_percentage: 0,
        });
        setCurrentStationId(null);
        setShowModal(false);
        fetchStations();
      }
    } catch (error) {
      console.error('Erro ao confirmar a coleta:', error);
    }
  };

  const handleVolumeChange = async (id, newVolumePercentage) => {
    try {
      await axios.patch(`http://127.0.0.1:8000/api/waste_stations/${id}/`, {
        volume_percentage: newVolumePercentage,
      });
      fetchStations();
    } catch (error) {
      console.error('Erro ao atualizar o volume:', error);
    }
  };

  useEffect(() => {
    fetchStations();
  }, []);

  const theme = createTheme({
    typography: {
      h4: {
        fontFamily: 'Roboto',
        fontSize: '4rem', // Aumentei o tamanho do título
        fontWeight: 700,
        color: '#333',
        marginBottom: '20px', // Adicionei margem inferior ao título
      },
    },
    palette: {
      background: {
        default: '#f5f5f5', // Alterei a cor de fundo para cinza claro
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <div style={{ textAlign: 'center', padding: '20px' }}>
        <Typography variant="h4">
        Estações de Resíduos
        </Typography>
        <Grid container spacing={2} justifyContent="center">
          {stations.map((station) => (
            <Grid item key={station.id} xs={12} sm={6} md={4}>
              <Paper elevation={3} style={{ padding: '20px', textAlign: 'center', marginBottom: '20px' }}>
                <Typography variant="h6">{station.name}</Typography>
                <Typography variant="body1">{`${station.volume_percentage}% Volume`}</Typography>
                <TextField
                  type="number"
                  label="Novo Volume (%)"
                  variant="outlined"
                  value={station.newVolumePercentage || ''}
                  onChange={(e) => {
                    const newVolume = parseInt(e.target.value, 10);
                    setStations((prevStations) =>
                      prevStations.map((prevStation) =>
                        prevStation.id === station.id
                          ? { ...prevStation, newVolumePercentage: newVolume }
                          : prevStation
                      )
                    );
                  }}
                />
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => handleVolumeChange(station.id, station.newVolumePercentage)}
                  style={{ marginTop: '10px' }}
                >
                  Atualizar Volume
                </Button>
                {showAutoCollectButton && station.volume_percentage >= 80 && (
                  <Button
                    variant="contained"
                    color="secondary"
                    onClick={() => handleCollectRequest(station.id)}
                    style={{ marginTop: '10px' }}
                  >
                    Coleta Automaticamente
                  </Button>
                )}
              </Paper>
            </Grid>
          ))}
        </Grid>
        {showModal && (
          <div className="modal" style={{ marginTop: '20px' }}>
            <div className="modal-content">
              <Typography variant="body1">
                A estação atingiu 80% de ocupação. Deseja confirmar a coleta?
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={handleCollectConfirmation}
                style={{ marginRight: '10px' }}
              >
                Confirmar Coleta
              </Button>
              <Button variant="contained" color="secondary" onClick={() => setShowModal(false)}>
                Cancelar
              </Button>
            </div>
          </div>
        )}
      </div>
    </ThemeProvider>
  );
};

export default WasteStationPage;



