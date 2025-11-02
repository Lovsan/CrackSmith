import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Grid,
  Button,
  Alert,
  Pagination,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Delete, Refresh } from '@mui/icons-material';
import { jobService } from '../services';

// Constants
const HASH_DISPLAY_LENGTH = 40;

const Jobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJobs();
  }, [page]);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const data = await jobService.getJobs(null, page, 10);
      setJobs(data.jobs);
      setTotalPages(data.pages);
    } catch (err) {
      setError('Failed to load jobs');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId) => {
    try {
      await jobService.deleteJob(jobId);
      fetchJobs();
    } catch (err) {
      setError('Failed to delete job');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'processing': return 'primary';
      default: return 'warning';
    }
  };

  const truncateHash = (hash) => {
    return hash.length > HASH_DISPLAY_LENGTH 
      ? `${hash.substring(0, HASH_DISPLAY_LENGTH)}...` 
      : hash;
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" fontWeight="bold">
          My Jobs
        </Typography>
        <Button startIcon={<Refresh />} onClick={fetchJobs}>
          Refresh
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Grid container spacing={2}>
        {jobs.map((job) => (
          <Grid item xs={12} key={job.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Box>
                    <Typography variant="h6">
                      {job.hash_type.toUpperCase()} Hash
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {truncateHash(job.hash_value)}
                    </Typography>
                    {job.result && (
                      <Typography variant="body2" color="success.main" mt={1}>
                        Password: {job.result}
                      </Typography>
                    )}
                    <Typography variant="caption" color="text.secondary">
                      Attempts: {job.attempts || 0}
                    </Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={2}>
                    <Chip label={job.status} color={getStatusColor(job.status)} />
                    {(job.status === 'queued' || job.status === 'failed') && (
                      <Tooltip title="Delete job">
                        <IconButton onClick={() => handleDelete(job.id)} color="error">
                          <Delete />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {totalPages > 1 && (
        <Box display="flex" justifyContent="center" mt={3}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={(e, value) => setPage(value)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
};

export default Jobs;
