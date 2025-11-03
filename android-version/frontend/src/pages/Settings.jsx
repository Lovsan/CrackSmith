import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Alert,
  Grid,
  Switch,
  FormControlLabel,
} from '@mui/material';
import { Lock } from '@mui/icons-material';
import { authService } from '../services';
import { useAuth } from '../context/AuthContext';

const Settings = () => {
  const { user, updateUser } = useAuth();
  const [pinData, setPinData] = useState({
    currentPin: '',
    newPin: '',
    confirmPin: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handlePinChange = (e) => {
    setPinData({
      ...pinData,
      [e.target.name]: e.target.value,
    });
  };

  const handlePinSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (pinData.newPin !== pinData.confirmPin) {
      setError('PIN codes do not match');
      return;
    }

    if (pinData.newPin.length < 4) {
      setError('PIN must be at least 4 characters');
      return;
    }

    setLoading(true);

    try {
      await authService.setPin(pinData.newPin, pinData.currentPin || null);
      setSuccess('PIN code updated successfully');
      setPinData({ currentPin: '', newPin: '', confirmPin: '' });
      updateUser();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update PIN');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Settings
      </Typography>

      <Grid container spacing={3}>
        {/* Account Information */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Account Information
              </Typography>
              
              <Box mt={2}>
                <Typography variant="body2" color="text.secondary">
                  Username
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {user?.username}
                </Typography>
              </Box>

              <Box mt={2}>
                <Typography variant="body2" color="text.secondary">
                  Email
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {user?.email}
                </Typography>
              </Box>

              <Box mt={2}>
                <Typography variant="body2" color="text.secondary">
                  Account Type
                </Typography>
                <Typography variant="body1" fontWeight="bold" color={user?.is_paid ? 'success.main' : 'text.primary'}>
                  {user?.is_paid ? 'Premium' : 'Free'}
                </Typography>
              </Box>

              <Box mt={2}>
                <Typography variant="body2" color="text.secondary">
                  Member Since
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Security Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                <Lock sx={{ mr: 1, verticalAlign: 'middle' }} />
                Security Settings
              </Typography>

              {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
              {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

              <form onSubmit={handlePinSubmit}>
                <TextField
                  fullWidth
                  label="Current PIN (if set)"
                  name="currentPin"
                  type="password"
                  value={pinData.currentPin}
                  onChange={handlePinChange}
                  margin="normal"
                />

                <TextField
                  fullWidth
                  label="New PIN"
                  name="newPin"
                  type="password"
                  value={pinData.newPin}
                  onChange={handlePinChange}
                  margin="normal"
                  required
                />

                <TextField
                  fullWidth
                  label="Confirm PIN"
                  name="confirmPin"
                  type="password"
                  value={pinData.confirmPin}
                  onChange={handlePinChange}
                  margin="normal"
                  required
                />

                <Button
                  fullWidth
                  type="submit"
                  variant="contained"
                  disabled={loading}
                  sx={{ mt: 2 }}
                >
                  {loading ? 'Updating...' : 'Update PIN'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </Grid>

        {/* App Preferences */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                App Preferences
              </Typography>

              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Enable notifications"
              />

              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Auto-refresh jobs"
              />

              <FormControlLabel
                control={<Switch />}
                label="Dark mode (always on)"
                disabled
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;
