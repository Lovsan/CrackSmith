import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Tabs,
  Tab,
  Alert,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { adminService } from '../services';

const Admin = () => {
  const { user } = useAuth();
  const [tabValue, setTabValue] = useState(0);
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [installations, setInstallations] = useState([]);

  useEffect(() => {
    if (user?.is_admin) {
      fetchAdminStats();
      fetchUsers();
      fetchInstallations();
    }
  }, [user]);

  const fetchAdminStats = async () => {
    try {
      const data = await adminService.getAdminStats();
      setStats(data);
    } catch (err) {
      console.error('Error fetching admin stats:', err);
    }
  };

  const fetchUsers = async () => {
    try {
      const data = await adminService.getUsers();
      setUsers(data.users);
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  };

  const fetchInstallations = async () => {
    try {
      const data = await adminService.getInstallations();
      setInstallations(data.installations);
    } catch (err) {
      console.error('Error fetching installations:', err);
    }
  };

  if (!user?.is_admin) {
    return (
      <Alert severity="error">
        You do not have permission to access this page.
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Admin Panel
      </Typography>

      <Grid container spacing={3}>
        {/* Overview Stats */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Users
              </Typography>
              <Typography variant="h4" fontWeight="bold">
                {stats?.users?.total || 0}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {stats?.users?.paid || 0} premium
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Jobs
              </Typography>
              <Typography variant="h4" fontWeight="bold">
                {stats?.jobs?.total || 0}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {stats?.jobs?.completed || 0} completed
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Installations
              </Typography>
              <Typography variant="h4" fontWeight="bold">
                {stats?.installations?.total || 0}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {stats?.installations?.active || 0} active
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                This Week
              </Typography>
              <Typography variant="h4" fontWeight="bold">
                {stats?.users?.new_this_week || 0}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                new users
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Detailed Information */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
                <Tab label="Users" />
                <Tab label="Installations" />
                <Tab label="Jobs" />
              </Tabs>

              <Box mt={3}>
                {tabValue === 0 && (
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      Recent Users
                    </Typography>
                    {users.slice(0, 10).map((u) => (
                      <Box
                        key={u.id}
                        sx={{
                          p: 2,
                          mb: 1,
                          border: '1px solid',
                          borderColor: 'divider',
                          borderRadius: 1,
                        }}
                      >
                        <Typography variant="body1" fontWeight="bold">
                          {u.username} ({u.email})
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Type: {u.is_paid ? 'Premium' : 'Free'} | 
                          Admin: {u.is_admin ? 'Yes' : 'No'} |
                          Joined: {new Date(u.created_at).toLocaleDateString()}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                )}

                {tabValue === 1 && (
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      Recent Installations
                    </Typography>
                    {installations.slice(0, 10).map((inst) => (
                      <Box
                        key={inst.id}
                        sx={{
                          p: 2,
                          mb: 1,
                          border: '1px solid',
                          borderColor: 'divider',
                          borderRadius: 1,
                        }}
                      >
                        <Typography variant="body2">
                          Device: {inst.device_id}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Platform: {inst.platform || 'N/A'} |
                          Version: {inst.version || 'N/A'} |
                          Last Active: {new Date(inst.last_active).toLocaleDateString()}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                )}

                {tabValue === 2 && (
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      Job Statistics
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6} sm={3}>
                        <Typography variant="body2" color="text.secondary">
                          Queued
                        </Typography>
                        <Typography variant="h6">
                          {stats?.jobs?.queued || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={6} sm={3}>
                        <Typography variant="body2" color="text.secondary">
                          Processing
                        </Typography>
                        <Typography variant="h6">
                          {stats?.jobs?.processing || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={6} sm={3}>
                        <Typography variant="body2" color="text.secondary">
                          Completed
                        </Typography>
                        <Typography variant="h6" color="success.main">
                          {stats?.jobs?.completed || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={6} sm={3}>
                        <Typography variant="body2" color="text.secondary">
                          Failed
                        </Typography>
                        <Typography variant="h6" color="error.main">
                          {stats?.jobs?.failed || 0}
                        </Typography>
                      </Grid>
                    </Grid>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Admin;
