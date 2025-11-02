import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Alert,
  Chip,
  LinearProgress,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  HourglassEmpty,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { jobService, statsService } from '../services';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const [hashValue, setHashValue] = useState('');
  const [hashType, setHashType] = useState('auto');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [stats, setStats] = useState(null);
  const [recentJobs, setRecentJobs] = useState([]);

  useEffect(() => {
    fetchStats();
    fetchRecentJobs();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await statsService.getUserStats();
      setStats(data.statistics);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const fetchRecentJobs = async () => {
    try {
      const data = await jobService.getJobs(null, 1, 5);
      setRecentJobs(data.jobs);
    } catch (err) {
      console.error('Error fetching recent jobs:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!hashValue.trim()) {
      setError('Please enter a hash value');
      return;
    }

    setLoading(true);

    try {
      const response = await jobService.createJob(
        hashValue,
        hashType === 'auto' ? null : hashType
      );
      setSuccess(`Job submitted successfully! Job ID: ${response.job.id}`);
      setHashValue('');
      fetchStats();
      fetchRecentJobs();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit job');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle color="success" />;
      case 'failed':
        return <Error color="error" />;
      case 'processing':
        return <SettingsIcon color="primary" />;
      default:
        return <HourglassEmpty color="warning" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      case 'processing':
        return 'primary';
      default:
        return 'warning';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Jobs
              </Typography>
              <Typography variant="h4" fontWeight="bold">
                {stats?.total_jobs || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Successful Cracks
              </Typography>
              <Typography variant="h4" fontWeight="bold" color="success.main">
                {stats?.successful_cracks || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Failed Attempts
              </Typography>
              <Typography variant="h4" fontWeight="bold" color="error.main">
                {stats?.failed_attempts || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Account Type
              </Typography>
              <Chip
                label={user?.is_paid ? 'Premium' : 'Free'}
                color={user?.is_paid ? 'success' : 'default'}
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Job Submission Form */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Submit New Hash
              </Typography>

              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}

              {success && (
                <Alert severity="success" sx={{ mb: 2 }}>
                  {success}
                </Alert>
              )}

              <form onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={8}>
                    <TextField
                      fullWidth
                      label="Hash Value"
                      value={hashValue}
                      onChange={(e) => setHashValue(e.target.value)}
                      placeholder="Enter hash to crack"
                      disabled={loading}
                    />
                  </Grid>

                  <Grid item xs={12} md={2}>
                    <FormControl fullWidth>
                      <InputLabel>Hash Type</InputLabel>
                      <Select
                        value={hashType}
                        label="Hash Type"
                        onChange={(e) => setHashType(e.target.value)}
                        disabled={loading}
                      >
                        <MenuItem value="auto">Auto-detect</MenuItem>
                        <MenuItem value="md5">MD5</MenuItem>
                        <MenuItem value="sha1">SHA1</MenuItem>
                        <MenuItem value="sha256">SHA256</MenuItem>
                        <MenuItem value="bcrypt">Bcrypt</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>

                  <Grid item xs={12} md={2}>
                    <Button
                      fullWidth
                      variant="contained"
                      type="submit"
                      disabled={loading}
                      sx={{ height: '56px' }}
                    >
                      {loading ? 'Submitting...' : 'Submit'}
                    </Button>
                  </Grid>
                </Grid>
              </form>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Jobs */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Recent Jobs
              </Typography>

              {recentJobs.length === 0 ? (
                <Typography color="text.secondary">
                  No jobs yet. Submit a hash to get started!
                </Typography>
              ) : (
                <Box>
                  {recentJobs.map((job) => (
                    <Box
                      key={job.id}
                      sx={{
                        p: 2,
                        mb: 2,
                        border: '1px solid',
                        borderColor: 'divider',
                        borderRadius: 2,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        {getStatusIcon(job.status)}
                        <Box>
                          <Typography variant="body2" fontWeight="bold">
                            {job.hash_type.toUpperCase()} Hash
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {job.hash_value.substring(0, 20)}...
                          </Typography>
                        </Box>
                      </Box>
                      <Chip
                        label={job.status}
                        color={getStatusColor(job.status)}
                        size="small"
                      />
                    </Box>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
