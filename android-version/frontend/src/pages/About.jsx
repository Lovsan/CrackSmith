import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Divider,
  Link,
} from '@mui/material';
import {
  Security,
  Speed,
  Cloud,
  AttachMoney,
} from '@mui/icons-material';

const About = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        About CrackSmith
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Welcome to CrackSmith
              </Typography>
              <Typography variant="body1" paragraph>
                CrackSmith is a professional hash cracking service designed to help security
                professionals, researchers, and authorized users recover passwords from various
                hash types. Our platform combines powerful cracking capabilities with a
                user-friendly mobile interface.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Security color="primary" sx={{ fontSize: 40, mb: 2 }} />
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Security First
              </Typography>
              <Typography variant="body2">
                We take security seriously. All data is encrypted, and we implement
                anti-abuse checks, PIN code protection, and secure authentication
                to protect your account and data.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Speed color="primary" sx={{ fontSize: 40, mb: 2 }} />
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Fast Performance
              </Typography>
              <Typography variant="body2">
                Premium users get access to high-performance servers with priority
                queue processing, allowing for faster hash cracking with more threads
                and resources.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Cloud color="primary" sx={{ fontSize: 40, mb: 2 }} />
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Flexible Deployment
              </Typography>
              <Typography variant="body2">
                Run the app locally for free with limited resources, or upgrade to
                premium for cloud-based processing on our fast servers with
                expanded capabilities.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <AttachMoney color="primary" sx={{ fontSize: 40, mb: 2 }} />
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Free & Premium Plans
              </Typography>
              <Typography variant="body2">
                Start with our free plan to test the platform. Upgrade to premium
                for priority queue access, faster servers, more threads, and
                higher rate limits.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Supported Hash Types
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" fontWeight="bold">MD5</Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" fontWeight="bold">SHA1</Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" fontWeight="bold">SHA256</Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" fontWeight="bold">Bcrypt</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Why Choose Us?
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Beautiful UI:</strong> Mobile-friendly, responsive design that works
                seamlessly on all devices.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Statistics Dashboard:</strong> Track your cracking success with
                detailed charts and metrics.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Queue System:</strong> Fair job processing with priority access
                for premium users.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Admin Panel:</strong> Comprehensive management tools for monitoring
                installations and user activity.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Legal Notice
              </Typography>
              <Typography variant="body2" color="text.secondary">
                This tool is intended for authorized security testing, research, and
                password recovery only. Users must have explicit permission to crack
                any hashes they submit. Misuse of this service is strictly prohibited.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Open Source
              </Typography>
              <Typography variant="body2">
                CrackSmith is open source! View the code on{' '}
                <Link
                  href="https://github.com/Lovsan/CrackSmith"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  GitHub
                </Link>
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default About;
